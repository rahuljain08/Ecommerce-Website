from django.shortcuts import render, redirect
from django.http import HttpResponse
from auth import forms
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User
# Create your views here.


class Login(LoginView):
	redirect_authenticated_user = True
	template_name = "auth/login.html"
	extra_context = {"page": "Login"}

	def get_success_url(self):
		return self.request.GET.get("next", "/")


class Logout(LogoutView):
	next_page = '/'


class Signup(View):

	def get(self, request):
		if request.user.is_authenticated:
			return redirect("/")
		else:
			context = {
				"form": forms.SignUpForm(),
			}

			return render(request, "auth/signup.html", context)


	def post(self, request):

		form = forms.SignUpForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/')

		else:
			context = {
				"forms": form,
				"message": "Failed Validation!"
			}

			return render(request, "auth/signup.html", context)

class Changepassword(PasswordChangeView):
	template_name = "auth/changepassword.html"
	extra_context = {"page": "Change Password"}
	success_url = "/"