from registration.views import RegistrationView
from treble_app.forms import UserProfileForm
from treble_app.models import UserProfile


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/treble/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user_profile'] = UserProfileForm
        return context

    form_class = UserProfileForm

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        pic = form_class.cleaned_data["picture"]
        new_profile = UserProfile.objects.create(user=new_user, picture=pic)
        new_profile.save()
        return new_user
