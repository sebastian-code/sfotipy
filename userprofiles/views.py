#from django.views.generic import View
from django.views.generic import TemplateView
#from django.http import HttpResponse

from django.shortcuts import render
from .forms import UserCreationEmailForm, EmailAuthenticationForm
from django.contrib.auth import login

# class LoginView(View):
	
# 	def get(self, request, *args, **kwargs):
# 		return HttpResponse('LoginView!!')

class LoginView(TemplateView):
	template_name = 'login.html'

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