from django import forms
from treble_app.models import Song, Comment, UserProfile
from django.contrib.auth.models import User


class SongForm(forms.ModelForm):
    song_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    track_name = forms.CharField(max_length=128)
    artist = forms.CharField(max_length=128)
    genre = forms.CharField(max_length=128)
    album = forms.CharField(max_length=128)
    no_of_recommendations = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # TODO Verify that this is actually correct, was previously a merge conflict
    recommended_songs = forms.ModelMultipleChoiceField(queryset=Song, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Song
        fields = ('track_name',)


class CommentForm(forms.ModelForm):
    message = forms.CharField(
        max_length=250, help_text="Please give a review.")

    class Meta:
        model = Comment
        exclude = ('comment_id', 'song_id', 'username', 'datetime',)


class RecommendationForm(forms.Form):
    # TODO populate queryset parameter with all songs matching a search performed by the user
    # TODO Verify that this is actually correct, was previously a merge conflict
    recommended_songs = forms.ModelMultipleChoiceField(queryset=Song, widget=forms.CheckboxSelectMultiple())

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "col-sm-6", "required": "required"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "col-sm-6"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "col-sm-6"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    favourites = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput)

    class Meta:
        model = UserProfile
        fields = ('picture', 'favourites')
