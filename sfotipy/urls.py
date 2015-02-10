from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from artists.views import ArtistDetailView
from artists.views import ArtistListView
from artists.views import AlbumListView
from albums.views import AlbumDetailView
from rest_framework import routers, serializers
from artists.views import ArtistViewSet
from albums.views import AlbumViewSet
from tracks.views import TrackViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sfotipy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tracks/(?P<title>[\w\-\W]+)/$', 'tracks.views.track_view', name='track_view'),
    url(r'^signup/$', 'userprofiles.views.signup', name='signup'),
    url(r'^signin/$', 'userprofiles.views.signin', name='signin'),
 	url(r'^artists/(?P<pk>[\d]+)/$', ArtistDetailView.as_view()),   
 	url(r'^artists/$', ArtistListView.as_view()),
 	url(r'^albums/$', AlbumListView.as_view()),
 	url(r'^albums/(?P<artists>[\w\-]+)/$', AlbumListView.as_view(), name="albums"),
 	# url(r'^albums/detail/(?P<pk>[\d]+)/$', AlbumDetailView.as_view()),
 	url(r'^albums/detail/(?P<artist_id>[\w\-]+)/$', AlbumDetailView.as_view()), 
 	url(r'^api/', include(router.urls)),
 	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
 	url(r'^', include('userprofiles.urls')),
)

urlpatterns += patterns('',
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)