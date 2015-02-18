from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

from django.views.generic.detail import DetailView
from django.views.generic import ListView

from albums.models import Album
from artists.models import Artist

from userprofiles.mixins import LoginRequiredMixin

class JsonResponseMixin(object):
	def response_handler(self):
		format = self.request.GET.get('format', None)

		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = self.get_data()
		return JsonResponse(data, safe=False)
		
class ArtistDetailView(LoginRequiredMixin, DetailView):
	model = Artist

	def get_template_names(self):
		return 'artists.html'

class ArtistListView(LoginRequiredMixin, ListView):
	model = Artist
	context_object_name = 'artists'
	template_name = 'artists.html'

class AlbumListView(LoginRequiredMixin, JsonResponseMixin, ListView):
	model = Album
	context_object_name = 'albums'
	template_name = 'albums.html'
	paginate_by = 2

	def get(self, request, *args, **kwargs):
		self.object_list = self.get_queryset()
		return self.response_handler()

	def get_data(self):
		data = [{
			'cover': album.cover.url,
			'title': album.title,
			'artist': album.artist.first_name,
		} for album in self.object_list]

		return data

	# def json_to_response(self):
	# 	data = list()
	# 	# for album in self.object_list:
	# 	# 	data.append({
	# 	# 		'cover': album.cover.url,
	# 	# 		'title': album.title,
	# 	# 		'artist': album.artist.first_name,
	# 	# 	})


	# 	return JsonResponse(data, safe=False)

	def get_queryset(self):
		if self.kwargs.get('artist'):
			queryset = self.model.objects.filter(artist__first_name__contains=self.kwargs['artist'])
			# queryset = Album.objects.filter(artist_slug=self.kwargs['artist'])
		else:
			queryset = super(AlbumListView, self).get_queryset()

		return queryset
	
from rest_framework import routers, serializers, viewsets

class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Artist
        fields = ('id','first_name', 'last_name', 'biography', 'favorite_songs')

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class =  ArtistSerializer
    paginate_by = 1

class AlbumDetailView(LoginRequiredMixin,  DetailView):
	model = Album
	template_name = 'album_detail.html'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		format = self.request.GET.get('format', None)
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def json_to_response(self):
		data = {
			'album':{
				'cover': self.object.cover.url,
				'title': self.object.title,
				'slug': self.object.slug,
				'artist': self.object.artist.nickname,
				'tracks': [t.title for t in self.objecto.track_set.all()]
			}
		}
		
		return JsonResponse(data, safe=False)

# class TopTrackListView(ListView):
# 	queryset = Tracks.objects.all()
# 	template_name = 'track_list.html'