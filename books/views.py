from django import forms
from django.shortcuts import redirect, render, get_object_or_404 # for returning rendered templates ASAP
from django.views.generic import View

import openai

from .models import Book
from .forms import NewBookForm
from .gpt_calls import call_gpt_write_book

    # "render" function takes the request object as its first argument
    # "render" function takes the template name as its second argument
    # "render" function's third (optional) argument is the context (a way for passing information into the templates aka .html files in the matching names)


def home(request):  
    
    #This function will be run when someone visits the "home" page of the website. 
    #"request" is an object that Django automatically gives you, filled with details about the user's visit
    
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books, 'user': request.user})

# def new_book(request):
#     user = request.user
#     if request.method == 'POST':
#         form = NewBookForm(request.POST)
#         if form.is_valid():
#             book = form.save(commit=False)

#             try:
#                 book = call_gpt_write_book(user, book)
#             except openai.InvalidRequestError as e:
#                 form.add_error(None, f'[API error]\n{e}')

#             if form.is_valid():
#                 book.save()
#                 return redirect('home')
#     else:
#         form = NewBookForm()
#     return render(request, 'new_book.html', {'form': form})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book_detail.html', {'book': book})

def about(request):
    #return HttpResponse('<h1> About View Test </h1>') # for testing
    return render(request, 'about.html')

def about_company(request):
    #return HttpResponse('<h1> About Company View Test </h1>') # for testing
    return render(request, 'about_company.html', {'company_name': 'West of the Sun'})

def user_profile(request):
    #return HttpResponse('<h1> User Profile Page Test </h1>') # for testing
    return render(request, 'user_profile.html')

class NewBookView(View):
    def render(self, request):
        return render(request, 'new_book.html', {'form': self.form})
 
    def post(self, request):
        user = request.user
        self.form = NewBookForm(request.POST)
        if self.form.is_valid():
            book = self.form.save(commit=False)
            try:
                book = call_gpt_write_book(user, book)
            except openai.InvalidRequestError as e:
                self.form.add_error("gpt_name", f'[API error]\n{e}')            
            if self.form.is_valid():
                book.save()
                return redirect('home')
            
        return self.render(request)
    
    def get(self, request):
        self.form = NewBookForm()
        return self.render(request)


     
 