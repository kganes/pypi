from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='a_index'),
    url(r'new$', views.newTask, name = 'a_new'),
    url(r'delete/(?P<id>\d+)$', views.deleteTask, name = 'a_delete'),
    url(r'^(?P<id>\d+)$', views.showTask, name = 'a_show'),
    url(r'^(?P<id>\d+)/submit$', views.editTask, name = 'a_edit'),
    
]