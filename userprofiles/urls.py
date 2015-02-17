from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

from userprofiles.views import LoginView, ProfileView

urlpatterns = patterns('',
	# url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'profile/$', ProfileView.as_view(), name='profile'),
	url(r'perfil/$', RedirectView.as_view(url='/profile/'), name='perfil'),
)