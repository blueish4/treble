import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'treble.settings')

import django
django.setup()
from treble_app.models import Song, Comment, UserProfile


def populate():

    # Lists of dictionaries containing Songs
    songs = [
        {"song_id": 1,
         "track_name": "Hymn For The Weekend",
         "artist": "Coldplay",
         "genre": "Alternative Rock",
         "album": "A Head Full Of Dreams",
         "no_of_recommendations": 2,
         "recommended_songs": [3, 5]},
        {"song_id": 2,
         "track_name": "Hysteria",
         "artist": "Muse",
         "genre": "Alternative Rock",
         "album": "Absolution",
         "no_of_recommendations": 1,
         "recommended_songs": [4]},
        {"song_id": 3,
         "track_name": "Fix You",
         "artist": "Coldplay",
         "genre": "Alternative Rock",
         "album": "X & Y",
         "no_of_recommendations": 2,
         "recommended_songs": [1, 5]},
        {"song_id": 4,
         "track_name": "ELEMENT.",
         "artist": "Kendrick Lamar",
         "genre": "Rap",
         "album": "DAMN.",
         "no_of_recommendations": 1,
         "recommended_songs": [2]},
        {"song_id": 5,
         "track_name": "Counting Stars",
         "artist": "OneRepublic",
         "genre": "Pop Rock",
         "album": "Native",
         "no_of_recommendations": 2,
         "recommended_songs": [1, 3]},
    ]

    # List of Comments dictionaries
    comments = [
        {"comment_id": 1,
         "song_id": 1,
         "username": "Sir Ri",
         "message": "This is a very good song.",
         "datetime": "01/03/18 12:53"},

        {"comment_id": 2,
         "song_id": 1,
         "username": "Alexa",
         "message": "I love this song!",
         "datetime": "01/03/18 12:56"},

        {"comment_id": 3,
         "song_id": 2,
         "username": "Sir Ri",
         "message": "This song is amazing!",
         "datetime": "01/03/18 13:00"},

        {"comment_id": 4,
         "song_id": 4,
         "username": "Bob",
         "message": "Kendrick is GOAT.",
         "datetime": "01/03/18 13:01"},

        {"comment_id": 5,
         "song_id": 5,
         "username": "Bob",
         "message": "Meh, it's okay I guess",
         "datetime": "01/03/18 13:02"}
    ]

    for i in range(len(songs)):
        # Add song from list above
        new_song = songs[i]
        s = add_song(new_song['song_id'], new_song['track_name'], new_song['artist'],
                     new_song['genre'], new_song['album'], new_song['no_of_recommendations'])
        for j in range(len(comments)):
            # If song_id ()
            new_comment = comments[j]
            if new_comment['song_id'] == s.song_id:
                add_comment(s, new_comment['comment_id'],
                            new_comment['username'], new_comment['message'], new_comment['datetime'])

    # Print out Songs that have been added
    for s in Song.objects.all():
        for c in Comment.objects.filter(song_id=s):
            print("- {0} - {1}".format(str(s), str(c)))


def add_song(song_id, track_name, artist, genre, album, no_of_recommendations):
    s = Song.objects.get_or_create(song_id=song_id, track_name=track_name)[0]
    s.track_name = track_name
    s.artist = artist
    s.genre = genre
    s.album = album
    s.no_of_recommendations = no_of_recommendations
    #s.recommended_songs = recommended_songs
    s.save()

    return s


def add_comment(song_id, comment_id, username, message, datetime):
    c = Comment.objects.get_or_create(
        song_id=song_id, comment_id=comment_id)[0]
    c.song_id = song_id
    c.username = username
    c.message = message
    c.datetime = datetime
    c.save()
    return c


if __name__ == '__main__':
    print("Starting population script...")
    populate()
