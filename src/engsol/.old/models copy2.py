from django.db import models
from account.models import Account

# Create your models here.

# Report
class Report(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Projeto
class Project(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=20)
    #description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Cliente
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    #phone = models.CharField(max_length=20)
    #address = models.CharField(max_length=100)
    #gender = models.CharField(max_length=20)
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
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    rank = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)