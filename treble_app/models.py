#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Song Model
class Song(models.Model):
    # Unique ID, and has a many-to-many relationship with itself
    song_id = models.IntegerField(primary_key=True)
    track_name = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    album = models.CharField(max_length=128)
    spotify_uri = models.CharField(max_length=256)
    artwork_url = models.CharField(max_length=256)
    no_of_recommendations = models.IntegerField(null=True)
    recommended_songs = models.ManyToManyField('self', symmetrical=False)

    comments = models.ManyToManyField("Comment", symmetrical=False)

    class Meta:
        unique_together = (("track_name", "artist"),)

    def __str__(self):
        return self.track_name


# User Model
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    username_slug = models.SlugField(unique=True)
    favourites = models.ManyToManyField(Song, symmetrical=False)
    picture = models.ImageField(upload_to='profile_images', blank=True, default="profile_images/default_pic.png")

    comments = models.ManyToManyField("Comment", symmetrical=False)

    def save(self, *args, **kwargs):
        self.username_slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


# Comment Model
class Comment(models.Model):
    # Unique Comment ID, and has foreign keys Song ID and Username
    # comment_id = models.IntegerField(primary_key=True)
    song_id = models.ForeignKey('Song', default=0)
    username = models.ForeignKey('UserProfile', default=1)
    message = models.CharField(max_length=256)
    datetime = models.DateTimeField(default=timezone.now, blank=False)

    # Reactions are between 0 and 5 where:
    #           0:     Smile Emoji (Default)
    #           1:     Love Emoji
    #           2:     Surprised Emoji
    #           3:     Relieved/Relaxed Emoji
    #           4:     Perfect Emoji
    #           5:     Dissapointed Emoji
    CHOICES = ((0, '☺️'),
               (1, '❤️'),
               (2, '😲'),
               (3, '😌'),
               (4, '👌'),
               (5, '😞'))
    reaction = models.IntegerField(default=0, choices=CHOICES)

    def __str__(self):
        return self.message
