from django.conf.urls import url, include
from treble_app import views
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page 
#if successful at logging 

class MyRegistrationView(RegistrationView):
	def get_success_url(self,user):
		return '/treble/'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/(?P<username_slug>[\w\-]+)/$',
        views.user_profile, name='user_profile'),
    url(r'^user/my-account$', views.user_account, name='user_account'),
    url(r'^song/(?P<song_id>[\d]+)/$', views.song, name='song'),
    url(r'^song/(?P<song_id>[\d]+)/comment/$', views.add_song_comment, name='song_comment'),
    url(r'^song/(?P<song_id>[\d]+)/add-recommendation/$', views.add_song_recommendation, name='song_recommendation'),
    url(r'^about-us/$', views.about, name='about'),
    url(r'^contact-us/$', views.contact, name='contact'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^accounts/register/$',
		MyRegistrationView.as_view(),
			name='registration_register'),
]
