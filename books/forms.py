from django import forms
from .models import Book


class NewBookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), max_length=1024,
                            help_text="Title of the book (not provided to GPT)")
    meta_prompt = forms.CharField(widget=forms.Textarea(attrs={"rows": 7}), max_length=4000,
                                  help_text="This is fed to GPT as context")
    initial_prompt = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), max_length=4000,
                                     help_text="Initial prompt for description creation")
    outline_prompt = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), max_length=4000,
                                     help_text="Prompt GPT for outline of the book (optional)",
                                     required=False)
    gpt_name = forms.CharField(
        label="GPT name",
        help_text="Type of GPT model to use",
        widget=forms.Select(
        choices=((x, x) for x in ("gpt-3.5-turbo", "gpt-4", "gpt-4-32k"))))

    class Meta:
        model = Book
        fields = ('gpt_name', 'title', 'meta_prompt', 'initial_prompt', 'outline_prompt')