from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=1024)
    title_prompt = models.CharField(max_length=1024, blank=True)
    title_gen = models.CharField(max_length=8192, blank=True)
    description = models.TextField()
    description_prompt = models.TextField(blank=True)
    description_gen = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    generated_at = models.DateTimeField(null=True)

class Chapter(models.Model):
    title = models.CharField(max_length=1024)
#    title_prompt = models.CharField(max_length=1024)
    title_gen = models.CharField(max_length=8192)
#    content = models.TextField()
    content_prompt = models.TextField()
    content_gen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    generated_at = models.DateTimeField(null=True)
    book = models.ForeignKey(Book, related_name='chapters',
                             on_delete=models.RESTRICT)

class Content(models.Model):
    final_content = models.TextField()
    chapter = models.ForeignKey(Chapter, related_name='chapters')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='contents')
    updated_by = models.ForeignKey(User, null=True, related_name='+')
