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
    context_dict = {"name": song_name_slug,
                    "artist": "Taylor Swift",
                    "img": "https://i.scdn.co/image/abd96549fa53000a633d64cbab5a69a623b6bdfa",
                    "spotify": "spotify:track:4vVb2D6RYL669h7tLYOKwx",
                    "similar": [{"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                                 "name": "This song here",
                                 "url": "/treble/song/this-song-here/"},
                                {"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                                 "name": "This song here",
                                 "url": "/treble/song/this-song-here/"},
                                {"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                                 "name": "This song here",
                                 "url": "/treble/song/this-song-here/"},
                                {"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                                 "name": "This song here",
                                 "url": "/treble/song/this-song-here/"},
                                {"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                                 "name": "This song here",
                                 "url": "https://127.0.0.1:8000/treble/song/this-song-here/"},
                                {"image": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
                                 "name": "This song here",
                                 "url": "/treble/song/this-song-here/"}
                                ],
                    "reviews": [{"reviewer_name": "Alice",
                                 "reaction": ":D",
                                 "review_text": "This is a really great song!"},
                                {"reviewer_name": "Alice",
                                 "reaction": ":D",
                                 "review_text": "This is a really great song!"},
                                {"reviewer_name": "Bob",
                                 "reaction": ":(",
                                 "review_text": "I am a massive fucking killjoy."}
                                ]
                    }
    return render(request, 'song.html', context=context_dict)

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
