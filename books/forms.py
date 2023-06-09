from django import forms
from .models import Book
from .gpt_calls import call_gpt_write_book


class NewBookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), max_length=1024,
                            help_text="Title of the book (not provided to GPT)")
    meta_prompt = forms.CharField(widget=forms.Textarea(attrs={"rows": 7}), max_length=8192,
                                  help_text="This is fed to GPT as context")
    initial_prompt = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), max_length=8192,
                                     help_text="Initial prompt for description creation")
    outline_prompt = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), max_length=8192,
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
    
    def save(self, user, commit=True):
        book = super(NewBookForm, self).save(commit=False)
        book = call_gpt_write_book(user, book)
        if commit:
            book.save()
        return book

class UpdateBookForm(NewBookForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}),
                                  max_length=8192,
                                  help_text="GPT-generated description")
    outline = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}),
                              max_length=8192,
                              help_text="GPT-generated outline",
                              required=False)

    class Meta:
        model = Book
        fields = ('gpt_name', 'title', 'meta_prompt', 'initial_prompt', 'description', 'outline_prompt', 'outline')