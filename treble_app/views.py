from django.shortcuts import render

# No need to import once all views return render()
from django.http import HttpResponse

def index(request):
    return HttpResponse('index')

def user_login(request):
    return HttpResponse('login')

def register(request):
    return HttpResponse('register')

def user_profile(request, username_slug):
    return HttpResponse('profile: ' + username_slug)

def user_account(request, username_slug):
    return HttpResponse('account: ' + username_slug)

def song(request, song_name_slug):
    return HttpResponse('song: ' + song_name_slug)

def song_comment(request, song_name_slug):
    return HttpResponse('comment: ' + song_name_slug)

def song_recommendation(request, song_name_slug):
    return HttpResponse('recommendation: ' + song_name_slug)

def about(request):
    return HttpResponse('about')

def contact(request):
    return HttpResponse('contact')

def faq(request):
    return HttpResponse('faq')

def user_logout(request):
    return HttpResponse('logout')
