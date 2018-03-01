from django.db import models

# Song Model
class Song(models.Model):
    # Unique ID, and has a many-to-many relationship with itself
    song_id = models.IntegerField(primary_key=True)
    track_name = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    album = models.CharField(max_length=128)
    no_of_recommendations = models.IntegerField(null=True)
    # recommended_songs = models.ManyToManyField('self')

    def __str__(self):
        return self.track_name

# User Model
class UserProfile(models.Model):
    # Unique Username
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.username

# Comment Model
class Comment(models.Model):
    # Unique Comment ID, and has foreign keys Song ID and Username
    comment_id = models.IntegerField(primary_key=True)
    song_id = models.ForeignKey(Song)
    username = models.CharField(max_length=20)  # To simplify population_script
    # username = models.ForeignKey(UserProfile)
    message = models.CharField(max_length=256)
    datetime = models.CharField(max_length=256)
    #datetime = models.DateField()

    def __str__(self):
        return self.message
