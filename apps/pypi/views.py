from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Task
from ..login.models import User
from django.contrib import messages
from datetime import datetime

def index(request):
	try:
		request.session['logged_in']
		user = User.objects.get(id=request.session['logged_in'])		
		today = datetime.today().date()
		context = {
			"users" : User.objects.get(id=request.session['logged_in']),
			"tasks" : Task.objects.all().order_by('date'),			
			"today": today
		}
		
		
		return render(request, 'pypi/index.html', context)
	except KeyError:
		return redirect(reverse('login_index'))


def newTask(request):
	try:
		request.session['logged_in']
		if request.method == "POST":
			user = User.objects.get(id=request.session['logged_in'])
			data=request.POST
			results = Task.objects.create(task=data['task'], status=data['status'], date=data['date'],time=data['time'], user=user)
			
			if results:
				return redirect(reverse('a_index'))
			else:
				errors = results[1]
				for error in errors:
					messages.error(request, error)
				return redirect(reverse('a_index'))
		else:
			return redirect(reverse('login_index'))	
	except KeyError:
		return redirect(reverse('login_index'))	
	
def showTask(request, id):
	try:
		request.session['logged_in']
		context = {
			"task": Task.objects.get(id=id)
		}
		return render(request, 'pypi/edit.html', context)
	except KeyError:
		return redirect(reverse('login_index'))

def editTask(request, id):
	try:
		request.session['logged_in']
		if request.method == "POST":

			task = Task.objects.get(id=id)
			print task
			task.status = request.POST['status']
			task.date = request.POST['date']
			task.time = request.POST['time']
			task.save()
			return redirect(reverse('a_show', kwargs={'id':id}))
		else: 
			return redirect(reverse('a_index'))
	except KeyError:
		return redirect(reverse('login_index'))

def deleteTask(request,id):
	try:
		if request.method == "POST":
			request.session['logged_in']
			task = Task.objects.get(id=id)
			task.delete()
			return redirect(reverse('a_index'))
		else:
			return redirect(reverse('a_index'))
	except KeyError:
		return redirect(reverse('login_index'))

	