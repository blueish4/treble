from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from treble_app.forms import UserForm, UserProfileForm, SongForm, CommentForm, RecommendationForm
from treble_app.models import Song, Comment


def index(request):
    most_recommended_songs = Song.objects.order_by('-no_of_recommendations')[:5]
    context_dict = {'most_recommended_songs': most_recommended_songs}

    return render(request, 'treble/index.html', context_dict)


def user_login(request):
    if request.method == 'POST':
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
                return render(request, 'treble/login.html', {'message': message})
        else:
            print("Invalid login details: {0}, {1}",
                  format(username, password))
            message = "Invalid login details supplied."
            return render(request, 'treble/login.html', {'message': message})
    else:
        message = ''
        return render(request, 'treble/login.html', {'message': message})


def register(request):
    # True if registration was successful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hash password and update user object
            user.set_password(user.password)
            user.save()

            # commit=False delays saving model, as user attributes must still be set
            profile = profile_form.save(commit=False)
            profile.user = user

            # Profile pic. supplied?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # Template registration was successful
            registered = True

        else:
            # Invalid form / mistakes
            print(user_form.errors, profile_form.errors)

    else:
        # Not HTTP POST so render blank form
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'treble/register.html', {'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'registered': registered})


@login_required  # Can only view other profiles if user is logged in
def user_profile(request, username_slug):
    user = UserProfile.objects.get(username=username_slug)
    return render(request, 'treble/user_profile.html', user)


@login_required
def user_account(request):
    user = request.user
    return render(request, 'treble/user_account.html', user)


def song(request, song_id):
    context_dict = {}
    # MICHAEL: This is the structure of the context dictionary I've written the template for.
    #          Ellipses indicate that the previous dictionary's structure is repeated
    # context_dict = {"name": song_name_slug,
    #                "artist": "Taylor Swift",
    #                "img": "https://i.scdn.co/image/abd96549fa53000a633d64cbab5a69a623b6bdfa",
    #                "spotify": "spotify:track:4vVb2D6RYL669h7tLYOKwx",
    #                "similar": [{"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
    #                             "name": "This song here",
    #                             "url": "/treble/song/this-song-here/"},...
    #                            ],
    #                "reviews": [{"reviewer_name": "Alice",
    #                             "reaction": ":D",
    #                             "review_text": "This is a really great song!"},...
    #                            ]
    #
    try:
        song_obj = Song.objects.get(song_id=song_id)
        comments = Comment.objects.get(song_id=song_id)
        context_dict['song'] = song_obj
        context_dict['comments'] = comments
    except Song.DoesNotExist:
        context_dict['song'] = None

    return render(request, 'treble/song.html', context_dict)


@login_required
def add_song(request):
    form = SongForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        # Redirect to homepage **FOR NOW**
        return HttpResponseRedirect(reverse('index'))
    else:
        print(form.errors)

    return render(request, 'treble/add_song.html', {'form': form})


@login_required
def add_song_comment(request, song_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        # Redirect to homepage **FOR NOW**
        return HttpResponseRedirect(reverse('index'))
    else:
        print(form.errors)
    return render(request, 'treble/add_comment.html', {'form': form})


@login_required
def add_song_recommendation(request, song_id):
    form = RecommendationForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        # Redirect to homepage **FOR NOW**
        return HttpResponseRedirect(reverse('index'))
    else:
        print(form.errors)

    return render(request, 'treble/add_recommendation.html', {'form': form})


def about(request):
    return render(request, 'treble/about.html', {})


def contact(request):
    return render(request, 'treble/contact.html', {})


def faq(request):
    return render(request, 'treble/faq.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
