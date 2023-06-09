from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=1024)
    gpt_name = models.CharField(max_length=1024)
    meta_prompt = models.TextField()
    initial_prompt = models.TextField()
    outline_prompt = models.TextField(blank=True)
    description = models.TextField(blank=True)
    outline = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_books")

class Chapter(models.Model):
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=1024)
    gpt_name = models.CharField(max_length=1024)
    chapter_prompt = models.TextField()
    content = models.TextField()
    revise_prompt = models.TextField(blank=True)
    revised_content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_chapters")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
