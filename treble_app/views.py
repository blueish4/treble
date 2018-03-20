from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from treble_app.forms import UserForm, UserProfileForm, SongForm, CommentForm, RecommendationForm
from treble_app.models import Song, Comment, UserProfile
from treble_app.spotify_search import search_spotify
from json import loads

import datetime

import json


def index(request):
    most_recommended_songs = Song.objects.order_by('-no_of_recommendations')[:5]
    context_dict = {'most_recommended_songs': most_recommended_songs}

    return render(request, 'treble/index.html', context_dict)


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST' and not request.user.is_authenticated():
        # Get username and password (returns None if unsuccessful)
        username = request.POST.get('username')
        password = request.POST.get('password')
        # User object returned if auth. is successful
        user = authenticate(username=username, password=password)

        if user:
            # Is user still active? (or disabled?)
            if user.is_active:
                # Log them in and redirect to homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                message = "Your Treble account is disabled."
                return render(request, 'registration/login.html', {'message': message})
        else:
            print("Invalid login details: "+username+" , "+password)
            message = "Invalid login details supplied."
            return render(request, 'registration/login.html', {'message': message})
    else:
        message = ''
        return render(request, 'registration/login.html', {'message': message})


def register(request):
    # a boolean value for telling te template
    # whether the registration was successful
    # set to false initially. code changes value to
    # true when registration succeeds
    registered = False

    # If its a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # attempt to grab information from raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.

            user.set_password(user.password)
            user.save()
            # now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so , we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # now we save the UserProfile model instance
            profile.save()

            # update our variable to indicate that the template
            # registration was successful
            registered = True
        else:
            # invalid form or forms - mistakes or something else?
            # print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    # render the template depending on the context.
    return render(request,
                  'registration/registration_form.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


@login_required  # Can only view other profiles if user is logged in
def user_profile(request, username_slug):
    user = UserProfile.objects.get(username_slug=username_slug)
    return render(request, 'treble/user_profile.html', {'profile': user})


@login_required
def user_account(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'treble/user_account.html', {'user': user, 'user_profile': user_profile})


def password_change(request):
    return render(request, 'registration/password_change_form.html', {})


def song(request, song_id):
    if int(song_id) < 1:
        return HttpResponseRedirect(reverse('index'))
    context_dict = {}

    try:
        song_obj = Song.objects.get(song_id=song_id)
        comments = Comment.objects.filter(song_id=song_id)
        context_dict['song'] = song_obj
        context_dict['recommended'] = song_obj.recommended_songs.all()
        context_dict['comments'] = comments

        # If a user has already reviewed a song they should only be able to edit the review
        # they shouldn't be able to leave another review.
        prev_comment_id = -1
        for comment in comments:
            if comment.username.id == request.user.id:
                prev_comment_id = comment.comment_id
                break

        if request.user.is_authenticated():
            if prev_comment_id == -1:
                context_dict['form'] = CommentForm(user=request.user, song_id=song_id)
                context_dict['edit'] = False
            else:
                comment = Comment.objects.get(comment_id=prev_comment_id)
                context_dict['form'] = CommentForm(user=request.user, song_id=song_id, instance=comment)
                context_dict['edit'] = True
                context_dict['prev_comment_id'] = prev_comment_id
            context_dict['add_song_form'] = SongForm(request.POST)

    except Song.DoesNotExist:
        # TODO Redirect to a 404 page instead
        context_dict['song'] = None
    context_dict['recommend_form'] = RecommendationForm(request.POST, song_id=song_id)
    return render(request, 'treble/song.html', context_dict)


@login_required
def add_song(request):
    form = SongForm(request.POST)
    if form.is_valid():
        saved = form.save(commit=True)
        song_id = Song.objects.get(spotify_uri=saved.spotify_uri, track_name=saved.track_name).song_id
        response = {"success": True,
                    "song_id": song_id,
                    "song_name": saved.track_name}
        return JsonResponse(response)
    else:
        print(form.errors)
        return HttpResponse(form.errors)


@login_required
def add_song_comment(request, song_id):
    # If the user isn't logged in, deny request
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('song', kwargs={"song_id": song_id}))

    form = CommentForm(request.POST, user=request.user, song_id=song_id)
    # Set the username and song id on the server side
    data_copy = form.data.copy()
    data_copy["song_id"] = str(song_id)
    data_copy["username"] = str(request.user.id)
    data_copy["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    form.data = data_copy
    if form.is_valid():
        form.save(commit=True)
    else:
        # TODO display errors somehow.
        # This might become easier if the form becomes an AJAX one, since it can be is the response body
        print(form.errors)
    return HttpResponseRedirect(reverse('song', kwargs={"song_id": song_id}))


@login_required
def edit_song_comment(request, song_id, comment_id):
    # If the user isn't logged in, deny request
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('song', kwargs={"song_id": song_id}))

    comment = Comment.objects.get(comment_id=comment_id)
    print(comment.comment_id,comment.message)
    form = CommentForm(request.POST, user=request.user, song_id=song_id, instance=comment)
    # Set the username and song id on the server side
    data_copy = form.data.copy()
    data_copy["song_id"] = str(song_id)
    data_copy["username"] = str(request.user.id)
    data_copy["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    form.data = data_copy
    if form.is_valid():
        form.save(commit=True)
    else:
        # TODO display errors somehow.
        # This might become easier if the form becomes an AJAX one, since it can be is the response body
        print(form.errors)
    return HttpResponseRedirect(reverse('song', kwargs={"song_id": song_id}))


@login_required
def add_song_recommendation(request, song_id):
    form = RecommendationForm(request.POST, song_id=song_id)
    data_copy = form.data.copy()
    data_copy['song_id'] = song_id
    form.data = data_copy
    if form.is_valid():
        song = Song.objects.get(song_id=song_id)
        for target in form.cleaned_data['recommended_songs']:
            song.recommended_songs.add(target)
        return HttpResponseRedirect(reverse('song', kwargs={"song_id": song_id}))
    else:
        # TODO RETURN JSON, esp. on errors
        print(form.errors)

    return render(request, 'treble/add_recommendation.html', {'form': form})


def spotify_lookup(request):
    return JsonResponse(search_spotify(request.GET.get("track"), "track"))


def about(request):
    return render(request, 'treble/about.html', {})


def contact(request):
    return render(request, 'treble/contact.html', {})


def faq(request):
    return render(request, 'treble/faq.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def navbar_search(request):
    search_term = request.GET.get('search_term', None)

    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()

    return_dict = []

    track_match = Song.objects.filter(track_name__contains=search_term)
    if track_match.exists():

        json_serializer.serialize(track_match)
        data = json.loads(json_serializer.getvalue())

        info = []
        for track in data:
            info.append({'track_name': track['fields']['track_name'], 'artist': track['fields']['artist'], "song_id": track['pk'], 'artwork_url': track['fields']['artwork_url']})

        return_dict.append({"label": info, "category": "Song", "logged_in": True})

    if request.user.is_authenticated():
        user_match = User.objects.filter(username__contains=search_term)
        if user_match.exists():

            json_serializer.serialize(user_match)
            data2 = json.loads(json_serializer.getvalue())
            profile = UserProfile.objects.get(user=user_match)

            info = [{"username": data2[0]['fields']['username'], "username_slug": profile.username_slug}]
            return_dict.append({"label": info, "category": "User", "logged_in": True })
    else:
        return_dict.append({"label": "You need to be logged in<br>to view users", "category": "User", "logged_in":False})

    return JsonResponse(return_dict, content_type="application/json", safe=False)
