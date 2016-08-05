from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from ..login.models import User

from datetime import datetime

class TaskManager(models.Manager):
	def createTask(self, data):
		error_flag = False
		errors = []

		if len(data['task']) < 1:
			errors.append("Task cannot be blank.")
			error_flag = True

		if len(data['date']) < 1:
			errors.append("Date cannot be blank.")
			error_flag = True
		elif datetime.today().date() > datetime.strptime(data['start_date'], '%Y-%m-%d').date():
			errors.append("Date cannot be in the past.")
			error_flag = True

		if len(data['time']) < 1:
			errors.append("Time cannot be blank.")
			error_flag = True

		if error_flag:
			return [False, errors]
		else:
			new_task = self.create(task=data['task'], status=data['status'], date=data['date'],time=data['time'], user=data['user'])
			return [True, new_task, new_task.id]


class Task(models.Model):
	task = models.CharField(max_length=255)
	date = models.DateField()
	time = models.TimeField()
	user = models.ForeignKey(User)
	status = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	taskManager = TaskManager()
	objects = models.Manager()

