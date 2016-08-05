from __future__ import unicode_literals
from django.db import models
from django.contrib import messages

import re
import bcrypt
from datetime import datetime

NAME_REGEX = re.compile(r'[a-zA-Z]+( [a-zA-Z0-9]+)*$')
EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z]).*\d$')

class UserManager(models.Manager):

	def register(self, userdata):
		error_flag = False
		errors = []

		if self.filter(email__exact=userdata['email']):
			errors.append("This email already exists.")
			error_flag = True

		if not EMAIL_REGEX.match(userdata['email']):
			errors.append("Invalid email address.")
			error_flag = True 		

		if len(userdata['name']) < 3:
			errors.append("Name must be at least 3 characters.")
			error_flag = True
		elif not NAME_REGEX.match(userdata['name']):
			errors.append("Name cannot contain numbers or symbols.")
			error_flag = True

		if len(userdata['password']) < 8:
			errors.append("Password must be at least 8 characters.")
			error_flag = True
		elif not PASSWORD_REGEX.match(userdata['password']):
			errors.append("Password must contain at least one uppercase letter and one number.")
			error_flag = True

		if len(userdata['passrepeat']) < 1:
			errors.append("Password confirmation cannot be blank.")
			error_flag = True
		elif not userdata['passrepeat'] == userdata['password']:
			errors.append("Passwords do not match!")
			error_flag = True

		if datetime.today().date() < datetime.strptime(userdata['dob'], '%Y-%m-%d').date():
			errors.append("Birthdate must be in the past.")
			error_flag = True

		password = userdata['password'].encode('utf-8')
		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		if error_flag:
			return [False, errors]
		else:
			user = self.create(name=userdata['name'], email=userdata['email'], dob=userdata['dob'], password=hashed)
			return [True, user, user.id]

	def login(self, data, request):
		error_flag = False
		errors = []
		person = self.filter(email__exact=data['email'])
		
		if person:
			person = person[0]
		else:
			errors.append("Invalid credentials.")
			error_flag = True
			return [False, errors]
		
		if person.password == bcrypt.hashpw(data['password'].encode('utf-8'), person.password.encode('utf-8')):
			request.session['logged_in'] = User.objects.get(email=data['email']).id
			return [True, person]
		else:
			errors.append("Invalid credentials.")
			error_flag = True
			return [False, errors]

class User(models.Model):
	name = models.CharField(max_length=45)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=100)
	dob = models.DateField()
	userManager = UserManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
