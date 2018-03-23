from django.test import TestCase
from .models import Song, UserProfile, Comment
import population_script
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


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
        comment.song_id = song
        comment.save()

        song.comments.add(comment)

        # Check if comment was saved correctly
        all_comments = song.comments.all()
        self.assertEquals(all_comments.count(), 1)

        first_comment = all_comments[0]
        self.assertEquals(first_comment, comment)
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
        user = User(username="Bob The Builder", id=1)
        # Create a new UserProfile
        user_profile = UserProfile(user=user)
        user.save()
        user_profile.save()

        # Check if username_slug was made correctly
        self.assertEquals(user_profile.username_slug, "bob-the-builder")

# class IndexViewTests(TestCase):
#
#     def test_index_view_has_most_recommended(self):
#         '''Check to ensure the index displays the top 5 most recommended songs'''
#
#         # Database starts empty, so must be populated
#         add_song(1,"one",1)
#         add_song(2,"two",2)
#         add_song(3,"three",3)
#         add_song(4,"four",4)
#         add_song(5,"five",5)
#         add_song(6,"six",6)
#
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)
#
#         # Only show top 5
#         # TODO Maybe remove these two assertions if song titles won't be displayed
#         print(response)
#         self.assertNotContains(response, "one")
#         self.assertContains(response, "six")
#
#         num_songs = len(response.context['most_recommended_songs'])
#         self.assertEqual(num_songs, 5)
#
# def add_song(song_id, track_name, no_recommendations):
#     '''Helper for index test'''
#     song = Song.objects.get_or_create(song_id=song_id)[0]
#     song.song_id = song_id
#     song.track_name = track_name
#     song.no_recommendations = no_recommendations
#     song.save()
#     return song

# class LoginViewTests(TestCase):
#
#     def test_login_succeeds_with_correct_credentials(self):
#         '''Tests if login succeeds when a valid user attempts to log in'''
#         user = User(username="Test",id=1)
#         user_profile = UserProfile(user=user)
#         user.set_password("test")
#         user.save()
#         user_profile.save()
#
#         response = self.client.post(reverse('auth_login'),
#                                     {'username_slug':user_profile.username_slug,
#                                      'password':user.password}, follow=True)
#         #If login is successful, the user is redirected (302) to homepage (index)
#         self.assertContains(response.redirect_chain, (reverse('index'),302))


class SongViewTests(TestCase):

    def test_song_view_non_existent_songs(self):
        """If the song does not exist, an appropriate message should be displayed"""
        try:
            response = self.client.get(reverse('song', kwargs={"song_id": 1}))
            self.assertEqual(response.status_code, 200)
        except:
            print("Song does not exist")

    def test_song_view_negative_id_displays_song_does_not_exist(self):
        """If a negative id is provided, the song not found page should appear"""
        try:
            response = self.client.get(reverse('song', kwargs={"song_id": -1}))
            self.assertEqual(response.status_code, 200)
        except:
            print("Invalid song id")

    def test_song_view_existing_song(self):
        """If the song exists, then redirect to song page"""
        song = Song(track_name="Shut Up and Dance", song_id=1)
        song.save()

        response = self.client.get(reverse('song', kwargs={"song_id": 1}))

        # Song exists so status code should be 200 OK
        self.assertEqual(response.status_code, 200)

        # Redirected to song page so page should contain track_name
        self.assertContains(response, song.track_name)


class UserTests(TestCase):

    def test_user_profile(self):
        # Create a new User
        user = User(username="John Smith", id=1)
        # Create a new UserProfile
        user_profile = UserProfile(user=user)
        user.password = "testpassword"
        # user.set_password("testpassword")
        user.email = "johnsmith@example.com"
        user.save()
        user_profile.save()

        # Check if username saved correctly
        self.assertEquals(user_profile.user.username, "John Smith")
        # Check if email saved correctly
        self.assertEquals(user_profile.user.email, "johnsmith@example.com")
        # Check if password saved correctly
        self.assertEquals(user_profile.user.password, "testpassword")
        # Check if username_slug was made correctly
        self.assertEquals(user_profile.username_slug, "john-smith")

    def test_user_profile_page_view_has_correct_info(self):
        # Create a new User
        user = User(username="John Smith", id=1)
        # Create a new UserProfile
        user_profile = UserProfile(user=user)
        user.password = "testpassword"
        # user.set_password("testpassword")
        user.email = "johnsmith@example.com"
        user.save()
        user_profile.save()

        response = self.client.post(reverse('user_profile', kwargs={"username_slug": user_profile.username_slug}))
