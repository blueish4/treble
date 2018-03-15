from django import forms
from treble_app.models import Song, Comment, UserProfile
from django.contrib.auth.models import User


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = ('song_id', 'recommended_songs', 'no_of_recommendations', 'comments')

    def __init__(self, *args, **kwargs):
        def text_input(length, **kwargs):
            return forms.CharField(max_length=length, widget=forms.TextInput(attrs={"class": "col-sm-9 form-control",
                                                                                    "autocomplete": "off"}), **kwargs)
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields['track_name'] = text_input(128, required=True)
        self.fields['artist'] = text_input(128, required=True)
        self.fields['genre'] = text_input(128)
        self.fields['album'] = text_input(128, required=True)
        self.fields['spotify_uri'] = text_input(128)
        self.fields['artwork_url'] = text_input(128)


class CommentForm(forms.ModelForm):
    message = forms.CharField(
        max_length=250, help_text="Please give a review.",
        widget=forms.Textarea(attrs={"class": "col-sm-9 form-control form-control-lg",
                                     "rows": 2}))
    reaction = forms.IntegerField(max_value=5, min_value=0, widget=forms.Select(choices=Comment.CHOICES,
                                                                                attrs={"class": "col-sm-9 form-control"}))

    class Meta:
        model = Comment
        exclude = ('comment_id', ) #'datetime')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        song_id = kwargs.pop('song_id', '')
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = "Comment"
        self.fields['username'] = forms.ModelChoiceField(
            queryset=UserProfile.objects.filter(user_id=user), initial=UserProfile.objects.none(),
            widget=forms.HiddenInput)
        self.fields['song_id'] = forms.ModelChoiceField(
            queryset=Song.objects.filter(song_id=song_id), initial=Song.objects.none(),
            widget=forms.HiddenInput)
        self.fields['datetime'] = forms.DateField(initial=datetime.date.today, widget=forms.HiddenInput)


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
