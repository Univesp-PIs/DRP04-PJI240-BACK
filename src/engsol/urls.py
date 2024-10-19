# Criar um arquivo igual o 'urls.py' do projeto
from django.urls import path, re_path
from . import views

urlpatterns = [

    # Project
    path('create_project', views.create_project, name='create_project'),
    path('update_project', views.update_project, name='update_project'),
    path('delete_project', views.delete_project, name='delete_project'),
    path('list_project', views.list_project, name='list_project'),

    # Status
    #path('create_status', views.create_status, name='create_status'),
    #path('update_status', views.update_status, name='update_status'),
    #path('delete_status', views.delete_status, name='delete_status'),
    #path('info_status', views.info_status, name='info_status')
    
]