from django import forms
from .models import Book


class NewBookForm(forms.ModelForm):
    meta_prompt = forms.CharField(widget=forms.Textarea(), max_length=4000)
    initial_prompt = forms.CharField(widget=forms.Textarea(), max_length=4000)
    gpt_name = forms.CharField(widget=forms.Select(
        choices=((x, x) for x in ("gpt-3.5-turbo", "gpt-4-32k"))))

    class Meta:
        model = Book
        fields = ('title', 'meta_prompt', 'initial_prompt', 'gpt_name')