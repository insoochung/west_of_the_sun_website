from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=1024)
    gpt_name = models.CharField(max_length=1024)
    meta_prompt = models.TextField()
    initial_prompt = models.TextField()
    description = models.TextField(blank=True)
    conversation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True)
    
class Chapter(models.Model):
    title = models.CharField(max_length=1024)
    title_prompt = models.CharField(max_length=1024)
    title_gen = models.CharField(max_length=8192)
    content = models.TextField()
    content_prompt = models.TextField()
    content_gen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    generated_at = models.DateTimeField(null=True)
    book = models.ForeignKey(Book, related_name='chapters',
                             on_delete=models.RESTRICT)
    