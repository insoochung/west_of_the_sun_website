from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=1024)
    title_prompt = models.CharField(max_length=1024)
    title_gen = models.CharField(max_length=8192)
    description = models.TextField()
    description_prompt = models.TextField()
    description_gen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    generated_at = models.DateTimeField(null=True)

class Chapter(models.Model):
    title = models.CharField(max_length=1024)
    title_prompt = models.CharField(max_length=1024)
    title_gen = models.CharField(max_length=8192)
    content = models.TextField()
    content_prompt = models.TextField()
    content_gen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    generated_at = models.DateTimeField(null=True)
    book = models.ForeignKey(Book, related_name='chapters')