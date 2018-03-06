import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'treble.settings')

import django
django.setup()
from treble_app.models import Song, Comment, UserProfile
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


def populate():

    # Lists of dictionaries containing Songs
    songs = [
        {"song_id": 1,
         "track_name": "Hymn For The Weekend",
         "artist": "Coldplay",
         "genre": "Alternative Rock",
         "album": "A Head Full Of Dreams",
         "recommended_songs": [3, 5]},
        {"song_id": 2,
         "track_name": "Hysteria",
         "artist": "Muse",
         "genre": "Alternative Rock",
         "album": "Absolution",
         "recommended_songs": [4]},
        {"song_id": 3,
         "track_name": "Fix You",
         "artist": "Coldplay",
         "genre": "Alternative Rock",
         "album": "X & Y",
         "recommended_songs": [1, 5]},
        {"song_id": 4,
         "track_name": "ELEMENT.",
         "artist": "Kendrick Lamar",
         "genre": "Rap",
         "album": "DAMN.",
         "recommended_songs": [2]},
        {"song_id": 5,
         "track_name": "Counting Stars",
         "artist": "OneRepublic",
         "genre": "Pop Rock",
         "album": "Native",
         "recommended_songs": [1, 3]},
    ]

    # List of dictionaries containing Users
    comments = [
        {"comment_id": 1,
         "song_id": 1,
         "username": "Sir Ri",
         "message": "This is a very good song."},

        {"comment_id": 2,
         "song_id": 1,
         "username": "Alexa",
         "message": "I love this song!"},

        {"comment_id": 3,
         "song_id": 2,
         "username": "Sir Ri",
         "message": "This song is amazing!"},

        {"comment_id": 4,
         "song_id": 4,
         "username": "Bob",
         "message": "Kendrick is GOAT."},

        {"comment_id": 5,
         "song_id": 5,
         "username": "Bob",
         "message": "Meh, it's okay I guess"}
    ]

    # List of dictionaries containing Users
    users = [
        {"username": "Sir Ri",
         "email": "sir_ri@example.com",
         "password": "abcde",
         "favourites": [1, 2]
         },
        {"username": "Alexa",
         "email": "alexa@example.com",
         "password": "12345",
         "favourites": [3, 4]
         },
        {"username": "Bob",
         "email": "bobby@example.com",
         "password": "bobby",
         "favourites": [5]
         }
    ]

    # Add all Songs
    for i in range(len(songs)):
        # Add song from list above
        new_song = songs[i]
        s = add_song(new_song['song_id'], new_song['track_name'], new_song['artist'],
                     new_song['genre'], new_song['album'])

    # Add all Users
    for i in range(len(users)):
        new_user = users[i]
        u = add_user(new_user['username'],
                     new_user['email'], new_user['password'], new_user['favourites'])

    # Add all comments
    for j in range(len(comments)):
        # Comments must be added after both Songs and Users
        new_comment = comments[j]
        song = Song.objects.get(song_id=new_comment['song_id'])
        add_comment(song, new_comment['comment_id'],
                    new_comment['username'], new_comment['message'])

    # Add recommended songs after all songs have been added
    for i in range(len(songs)):
        song = songs[i]
        for recommend in song['recommended_songs']:
            add_recommendation(song['song_id'], recommend)


    # Print out Users that have been added
    print("Users added... \n")
    for u in UserProfile.objects.all():
        print("Username: " + u.user.username)
        print("     --Email: " + u.user.email)
        print("     --Slug Username: " + u.username_slug)
        print("     --Favourites: ")
        for s in u.favourites.all():
            print("         - " + str(s))
        print("")

    # Print out Songs that have been added
    print("Songs added... \n")
    for s in Song.objects.all():
        print("Track Name: " + str(s))
        print("--Song Id: " + str(s.song_id))
        print("--Artist: " + s.artist)
        print("--Genre: " + s.genre)
        print("--Album: " + s.album)
        print("--Number of Recommendations: " +
              str(s.recommended_songs.count()))
        print("--Recommended Songs: ")
        for song in s.recommended_songs.all():

            print("        -" + str(song))
        print("")

    # Print out Comments that have been added, to which song, and by whom
    print("Comments added... \n")
    for s in Song.objects.all():
        print("Track Name: " + str(s))
        for c in Comment.objects.filter(song_id=s):
            print("     --" + str(c))
            print("         -" + str(c.username.user.username))
            print("         -" + str(c.datetime))
        print("")


def add_user(username, email, password, favourites):
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password)
    user.save()
    slug_username = slugify(username)
    u = UserProfile.objects.get_or_create(
        username_slug=slug_username, user_id=user.id)[0]
    for fav in favourites:
        u.favourites.add(Song.objects.get(song_id=fav))
    u.save()
    return u
  
  
def add_song(song_id, track_name, artist, genre, album):
    s = Song.objects.get_or_create(song_id=song_id, track_name=track_name)[0]
    s.track_name = track_name
    s.artist = artist
    s.genre = genre
    s.album = album
    s.save()
    return s


def add_recommendation(add_to, recommendation):
    s = Song.objects.get(song_id=add_to)
    to_add = Song.objects.get(song_id=recommendation)
    s.recommended_songs.add(to_add)
    s.save()
    return True


def add_comment(song_id, comment_id, username, message):
    c = Comment.objects.get_or_create(
        song_id=song_id, comment_id=comment_id)[0]
    c.song_id = song_id
    slug_username = slugify(username)
    u = UserProfile.objects.get(username_slug=slug_username)
    c.username = u
    c.message = message
    c.save()
    return c


if __name__ == '__main__':
    print("Starting population script... \n")
    populate()
