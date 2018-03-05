from django import forms
from rango.models import Song, Comment, UserProfile
from django.contrib.auth.models import User

class SongForm(forms.ModelForm):
    song_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    track_name = forms.CharField(max_length=128)
    artist = forms.CharField(max_length=128)
    genre = forms.CharField(max_length=128)
    album = forms.CharField(max_length=128)
    no_of_recommendations = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    recommended_songs = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Category
        fields = ('track_name',)

class CommentForm(forms.ModelForm):
    pass

class RecommendationForm():
    pass

class UserForm():
    pass

class UserProfileForm():
    pass
