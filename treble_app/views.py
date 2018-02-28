from django.shortcuts import render
from treble_app.models import Song
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# No need to import HttpResponse once all views return render()
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    most_recommended_songs = Song.objects.order_by('-recommendations')[:5]
    context_dict = {'most_recommended_songs', most_recommended_songs}

    return render(request, 'treble/index.html', context_dict)

def user_login(request):
    if request.method == 'POST':
        # Get username and password (returns None if unsuccessful)
        username = request.POST.get('username')
        password = request.POST.get('password')

        # User object returned if auth. is successful
        user = authenticate (username=username, password=password)

        if user:
            # Is user still active? (or disabled?)
            if user.is_active:
                # Log them in and redirect to homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                message = "Your Treble account is disabled."
                return render(request, 'treble/login.html' {'message':message})
        else:
            print("Invalid login details: {0}, {1}", format(username, password))
            message = "Invalid login details supplied."
            return render(request, 'treble/login.html', {'message':message})
    else:
        message = ''
        return render(request, 'rango/login.html', {'message':message})
    return HttpResponse('login')

def register(request):
    return HttpResponse('register')

def user_profile(request, username_slug):
    return HttpResponse('profile: ' + username_slug)

def user_account(request, username_slug):
    return HttpResponse('account: ' + username_slug)

def song(request, song_name_slug):
    context_dict = {}

    try:
        song = Song.objects.get(slug=song_name_slug)
        context_dict['song'] = song

    except Song.DoesNotExist:
        context_dict['song'] = None

    return render(request, 'rango/song.html', context_dict)

@login_required
def add_song(request):
    form = SongForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        # Redirect to homepage **FOR NOW**
        return HttpResponseRedirect(reverse('index'))
    else:
        print(form.errors)

    # Handles bad form, new form, or no form supplied cases and provides error message
    return render(request,'rango/add_song.html', {'form':form})

def song_comment(request, song_name_slug):
    return HttpResponse('comment: ' + song_name_slug)

def song_recommendation(request, song_name_slug):
    return HttpResponse('recommendation: ' + song_name_slug)

def about(request):
    context_dict = {}
    return render(request, 'treble/about.html', context_dict)

def contact(request):
    return HttpResponse('contact')

def faq(request):
    return HttpResponse('faq')

def user_logout(request):
    return HttpResponse('logout')
