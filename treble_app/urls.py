from django.conf.urls import url, include
from treble_app import views
from treble_app.registration_view import MyRegistrationView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<username_slug>[\w\-]+)/$',
        views.user_profile, name='user_profile'),
    url(r'^user/my-account$', views.user_account, name='user_account'),
    url(r'^user/my-account/add-favourite/$', views.add_favourite, name='add_favourite'),
    url(r'^song/(?P<song_id>[\w\-]+)/$', views.song, name='song'),
    url(r'^song/(?P<song_id>[\d]+)/comment/$', views.add_song_comment, name='song_comment'),
    url(r'^song/(?P<song_id>[\d]+)(?P<comment_id>[\d]+)/edit-comment/$',views.edit_song_comment, name='edit_comment'),
    url(r'^song/(?P<song_id>[\d]+)/add-recommendation/$', views.add_song_recommendation, name='song_recommendation'),
    url(r'^about-us/$', views.about, name='about'),
    url(r'^contact-us/$', views.contact, name='contact'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^most_recommended/$', views.most_recommended, name='most_recommended'),
    url(r'^accounts/register/$', MyRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/password/change/$', views.password_change, name='password_change'),
    url(r'^ajax/spotify/$', views.spotify_lookup, name='spotify_search'),
    url(r'^add_song/$', views.add_song, name='add_song'),
    url(r'^ajax/navbar_search/$', views.navbar_search, name='navbar_search'),
]
