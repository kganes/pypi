from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import User
from django.contrib import messages

def index(request):
	try:
		request.session['logged_in']
		return redirect(reverse('a_index'))
	except KeyError:
		return render(request, 'login/index.html')

def createUser(request):
	if request.method == "POST":
		results = User.userManager.register(request.POST)

		if results[0]:
			messages.success(request, "Success! Please login.")
			return redirect(reverse('login_index'))
		else:
			errors = results[1]
			for error in errors:
				messages.error(request, error)
			return redirect(reverse('login_index'))
	else:
		return redirect(reverse('login_index'))

def login(request):
	if request.method == "POST":
		results = User.userManager.login(request.POST, request)
		if results[0]:
			error_flag = True
			if 'logged_in' not in request.session:
				email = request.POST['email']
				request.session['logged_in'] = User.objects.get(email=email).id
				return redirect(reverse('a_index'))
			else:
				return redirect(reverse('login_index'))
		else:
			error_flag = False
			errors = results[1]
			for error in errors:
				messages.error(request, error)
			return redirect (reverse('login_index'))
	else:
		return redirect (reverse('login_index'))

def logout(request):
	request.session.clear()
	return redirect (reverse('login_index'))
