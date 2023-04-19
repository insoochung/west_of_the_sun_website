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
    updated_at = models.DateTimeField(null=True, blank=True)
#    updated_by = models.ForeignKey(User, null=True, related_name='+')
    generated_at = models.DateTimeField(null=True)
    
class Chapter(models.Model):
    title = models.CharField(max_length=1024)
    title_prompt = models.CharField(max_length=1024)
    title_gen = models.CharField(max_length=8192)
    content = models.TextField()
    content_prompt = models.TextField()
    content_gen = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
#    updated_by = models.ForeignKey(User, null=True, related_name='+')
    generated_at = models.DateTimeField(null=True)
    book = models.ForeignKey(Book, related_name='chapters',
                             on_delete=models.RESTRICT)
    