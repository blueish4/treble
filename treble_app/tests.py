from django.test import TestCase
from .models import Song, UserProfile, Comment
import population_script
from django.contrib.auth.models import User


class ModelTests(TestCase):

    def test_add_a_new_song(self):
        song = Song(track_name="Shut Up and Dance", song_id=1)
        song.save()

        # Check Song is in database
        songs_in_database = Song.objects.all()
        self.assertEquals(len(songs_in_database), 1)
        in_database = songs_in_database[0]
        self.assertEquals(in_database, song)


    def test_add_comment_to_song(self):
        song = Song(track_name="Shut Up and Dance", song_id=1)
        song.save()

        comment = Comment(comment_id=1, message="Overplayed song")
        comment.song_id=song
        comment.save()

        song.comments.add(comment)

        # Check if comment was saved correctly
        all_comments = song.comments.all()
        self.assertEquals(all_comments.count(),1)

        first_comment = all_comments[0]
        self.assertEquals(first_comment,comment)
        self.assertEquals(first_comment.message, "Overplayed song")

    def test_population_script(self):

        population_script.populate()

        # Check if Songs have correct metadata
        song = Song.objects.get(track_name="Hymn For The Weekend")
        self.assertEquals(song.artist, "Coldplay")
        self.assertEquals(song.genre, "Alternative Rock")
        self.assertEquals(song.album, "A Head Full Of Dreams")

        song = Song.objects.get(track_name="Hysteria")
        self.assertEquals(song.artist, "Muse")
        self.assertEquals(song.genre, "Alternative Rock")
        self.assertEquals(song.album, "Absolution")

        song = Song.objects.get(track_name="Fix You")
        self.assertEquals(song.artist, "Coldplay")
        self.assertEquals(song.genre, "Alternative Rock")
        self.assertEquals(song.album, "X & Y")

        song = Song.objects.get(track_name="ELEMENT.")
        self.assertEquals(song.artist, "Kendrick Lamar")
        self.assertEquals(song.genre, "Rap")
        self.assertEquals(song.album, "DAMN.")

        song = Song.objects.get(track_name="Counting Stars")
        self.assertEquals(song.artist, "OneRepublic")
        self.assertEquals(song.genre, "Pop Rock")
        self.assertEquals(song.album, "Native")

        # Check if Comments have been added to relevent User comments list
        for comment in Comment.objects.all():
            for user in UserProfile.objects.all():
                for user_comment in user.comments.all():
                    if comment.comment_id == user_comment.comment_id:
                        self.assertEquals(comment, user_comment)


    def test_user_slug_working(self):
        # Create a new User
        user = User(username="Bob The Builder",id=1)
        # Create a new UserProfile
        user_profile = UserProfile(user=user)
        user.save()
        user_profile.save()

        # Check if username_slug was made correctly
        self.assertEquals(user_profile.username_slug, "bob-the-builder")
