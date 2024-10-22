# Criar um arquivo igual o 'urls.py' do projeto
from django.urls import path, re_path
from . import views

urlpatterns = [

    # Project
    path('create_project', views.create_project, name='create_project'),
    path('update_project', views.update_project, name='update_project'),
    path('delete_project', views.delete_project, name='delete_project'),
    path('info_project', views.info_project, name='info_project'),
    path('list_project', views.list_project, name='list_project'),

    # Condition
    path('create_condition', views.create_condition, name='create_condiotion'),
    path('update_condition', views.update_condition, name='update_condition'),
    path('delete_condition', views.delete_condition, name='delete_condition'),
    path('list_condition', views.list_condition, name='list_condition'),
    
    # Note
    path('create_note', views.create_note, name='create_note'),
]