#from django.views.generic import View
from django.views.generic import TemplateView, RedirectView, FormView
#from django.http import HttpResponse

from django.shortcuts import render
from .forms import UserCreationEmailForm, EmailAuthenticationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from userprofiles.mixins import LoginRequiredMixin

# Se comentan las siguientes importaciones por no requerirse 
# al se reemplazas por el mixin del app
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator

class LoginView(FormView):
	form_class = AuthenticationForm
	template_name = 'login.html'
	success_url = '/profile/'
	
	def form_valid(self, form):
		# username = form.cleaned_data['username']
		# password = form.cleaned_data['password']
		# user = authenticate(username=username, password=password)
		login(self.request, form.user_cache)

		return super(LoginView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		is_auth = False
		name = None

		if self.request.user.is_authenticated():
			is_auth = True
			name = self.request.user.username

		data = {
			'is_auth': is_auth,
			'name': name,
		}

		context.update(data)
		return context

# class LoginView(TemplateView):
# 	template_name = 'login.html'

# 	def get_context_data(self, **kwargs):
# 		context = super(LoginView, self).get_context_data(**kwargs)
# 		is_auth = False
# 		name = None

# 		if self.request.user.is_authenticated():
# 			is_auth = True
# 			name = self.request.user.username

# 		data = {
# 			'is_auth': is_auth,
# 			'name': name,
# 		}

# 		context.update(data)
# 		return context

class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'profile.html'

	#Se comenta para incorporarse en el mixin
	# @method_decorator(login_required(login_url='/login/'))
	# def dispatch(self, request, *args, **kwargs):
	#     return super(ProfileView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)

		if self.request.user.is_authenticated():
			context.update({'userprofile': self.get_userprofile()})

		return context

	def get_userprofile(self):
		return self.request.user.userprofile

def signup(request):
	form = UserCreationEmailForm(request.POST or None)

	if form.is_valid():
		form.save()

	return render(request, 'signup.html', {'form': form})

def signin(request):
	form = EmailAuthenticationForm(request.POST or None)

	if form.is_valid():
		login(request, form.get_user())

	return render(request, 'signin.html', {'form': form})