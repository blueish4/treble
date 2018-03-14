from django.conf.urls import url
from treble_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/(?P<username_slug>[\w\-]+)/$',
        views.user_profile, name='user_profile'),
    url(r'^user/my-account$', views.user_account, name='user_account'),
    url(r'^song/(?P<song_id>[\w\-]+)/$', views.song, name='song'),
    url(r'^song/(?P<song_id>[\d]+)/comment/$', views.add_song_comment, name='song_comment'),
    url(r'^song/(?P<song_id>[\d]+)/add-recommendation/$', views.add_song_recommendation, name='song_recommendation'),
    url(r'^about-us/$', views.about, name='about'),
    url(r'^contact-us/$', views.contact, name='contact'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^search/(?P<search_term>[a-zA-Z0-9\s]*)$', views.search, name='search'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^ajax/spotify/$', views.spotify_lookup, name='spotify_search'),
    url(r'^add_song/$', views.add_song, name='add_song'),
    url(r'^ajax/navbar_search/$', views.navbar_search, name='navbar_search'),
]
