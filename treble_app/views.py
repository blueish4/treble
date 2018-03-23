from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from treble_app.forms import SongForm, CommentForm, RecommendationForm, FavouriteForm
from treble_app.models import Song, Comment, UserProfile
from treble_app.spotify_search import search_spotify

import datetime

import json


def index(request):
    comment_list = Comment.objects.order_by('-datetime')
    recently_reviewed = []
    for comment in comment_list:
        song_obj = Song.objects.filter(track_name=comment.song_id)

        if song_obj[0] not in recently_reviewed:
            recently_reviewed += song_obj

        if len(recently_reviewed) == 5:
            break

    recently_added = Song.objects.order_by('-song_id')[:5]
    context_dict = {'recently_reviewed': recently_reviewed,
                    'comments': comment_list,
                    "recently_added": recently_added,
					'add_song_form': SongForm()}
    return render(request, 'treble/index.html', context_dict)


def most_recommended(request):
    song_list = Song.objects.order_by('-no_of_recommendations')[:5]
    context_dict = {'songs': song_list,
                    'add_song_form': SongForm()}
    return render(request, 'treble/most_recommended.html', context_dict)


@login_required  # Can only view other profiles if user is logged in
def user_profile(request, username_slug):
    user = UserProfile.objects.get(username_slug=username_slug)
    return render(request, 'treble/user_profile.html', {'profile': user,
                                                        'add_song_form': SongForm()})


@login_required
def user_account(request):
    user = request.user
    users_profile = UserProfile.objects.get(user=user)
    context_dict = {'add_song_form': SongForm(),
                    'user': user, 'user_profile': users_profile}

    rec_dict = {}
    for fave in users_profile.favourites.all():
        for rec_song in fave.recommended_songs.all():
            if rec_song in rec_dict.keys():
                rec_dict[rec_song].append(fave)
            else:
                rec_dict[rec_song] = [fave]

    context_dict['rec_dict'] = rec_dict
    context_dict['favourite_form'] = FavouriteForm(request.POST, username_slug=users_profile.username_slug)
    return render(request, 'treble/user_account.html', context_dict)


def password_change(request):
    return render(request, 'registration/password_change_form.html', context={'add_song_form': SongForm()})


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
                prev_comment_id = comment.pk
                break

        if request.user.is_authenticated():
            if prev_comment_id == -1:
                context_dict['form'] = CommentForm(user=request.user, song_id=song_id)
                context_dict['edit'] = False
            else:
                comment = Comment.objects.get(pk=prev_comment_id)
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
        inst = form.save(commit=False)
        inst.pk = None
        inst.save()
        UserProfile.objects.get(user=request.user).comments.add(inst)
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

    comment = Comment.objects.get(pk=comment_id)
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
        song_obj = Song.objects.get(song_id=song_id)
        for target in form.cleaned_data['recommended_songs']:
            song_obj.recommended_songs.add(target)
        return HttpResponseRedirect(reverse('song', kwargs={"song_id": song_id}))
    else:
        # TODO RETURN JSON, esp. on errors
        print(form.errors)

    return JsonResponse({"errors": form.errors})


def add_favourite(request):
    user = request.user
    users_profile = UserProfile.objects.get(user=user)
    form = FavouriteForm(request.POST, username_slug=users_profile.username_slug)
    data_copy = form.data.copy()
    data_copy['user'] = users_profile.username_slug
    form.data = data_copy

    if form.is_valid():
        for target in form.cleaned_data['favourites']:
            users_profile.favourites.add(target)
        return HttpResponseRedirect(reverse('user_account'))
    else:
        print(form.errors)

    return render(request, 'treble/user_account.html', {'form': form, 'add_song_form': SongForm()})


def spotify_lookup(request):
    return JsonResponse(search_spotify(request.GET.get("track"), "track"))


def about(request):
    return render(request, 'treble/about.html', {'add_song_form': SongForm()})


def contact(request):
    return render(request, 'treble/contact.html', {'add_song_form': SongForm()})


def faq(request):
    return render(request, 'treble/faq.html', {'add_song_form': SongForm()})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def navbar_search(request):
    search_term = request.GET.get('search_term', None)

    jsonserializer = serializers.get_serializer("json")
    json_serializer = jsonserializer()

    return_dict = []

    track_match = Song.objects.filter(track_name__contains=search_term)
    if track_match.exists():

        json_serializer.serialize(track_match)
        data = json.loads(json_serializer.getvalue())

        info = []
        for track in data:
            info.append({'track_name': track['fields']['track_name'],
                         'artist': track['fields']['artist'],
                         "song_id": track['pk'],
                         'artwork_url': track['fields']['artwork_url']})

        return_dict.append({"label": info, "category": "Song", "logged_in": True})

    if request.user.is_authenticated():
        user_match = User.objects.filter(username__contains=search_term)
        if user_match.exists():

            json_serializer.serialize(user_match)
            data2 = json.loads(json_serializer.getvalue())
            profile = UserProfile.objects.get(user=user_match)

            info = [{"username": data2[0]['fields']['username'], "username_slug": profile.username_slug}]
            return_dict.append({"label": info, "category": "User", "logged_in": True})
    else:
        return_dict.append({"label": "You need to be logged in<br>to view users",
                            "category": "User", "logged_in": False})

    return JsonResponse(return_dict, content_type="application/json", safe=False)
