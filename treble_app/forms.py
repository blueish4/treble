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
    spotify_uri = forms.CharField(max_length=256)
    artwork_url = forms.CharField(max_length=256)
    recommended_songs = forms.ModelMultipleChoiceField(queryset=Song, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Song
        fields = ('track_name',)


class CommentForm(forms.ModelForm):
    message = forms.CharField(
        max_length=250, help_text="Please give a review.", widget=forms.Textarea(attrs={"class": "col-sm-6", "rows": 3}))
    reaction = forms.IntegerField(max_value=5, min_value=0, widget=forms.Select(choices=Comment.CHOICES))

    class Meta:
        model = Comment
        exclude = ('comment_id', 'datetime')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        song_id = kwargs.pop('song_id', '')
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(user_id=user), initial=UserProfile.objects.none(),
            widget=forms.HiddenInput)
        self.fields['song_id'] = forms.ModelChoiceField(
            queryset=Song.objects.filter(song_id=song_id), initial=Song.objects.none(),
            widget=forms.HiddenInput)


class RecommendationForm(forms.Form):
    # TODO populate queryset parameter with all songs matching a search performed by the user
    recommended_songs = forms.ModelMultipleChoiceField(queryset=Song, widget=forms.CheckboxSelectMultiple())

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "col-sm-6", "required": "required"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "col-sm-6"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "col-sm-6"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture',)
