from django.db import models
from account.models import Credential

# Create your models here.

# Projeto
class Project(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Cliente
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Status
class Status(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Ranking
class Ranking(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    rank = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)