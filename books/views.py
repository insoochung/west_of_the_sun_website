from django.shortcuts import redirect, render, get_object_or_404 # for returning rendered templates ASAP
from django.views.generic import View, UpdateView, DeleteView, DetailView
from django.utils import timezone
from django.http import HttpResponseRedirect

import openai

from .models import Book, Chapter
from .forms import NewBookForm, UpdateBookForm, NewChapterForm, UpdateChapterForm
from .gpt_calls import call_gpt_write_book

    # "render" function takes the request object as its first argument
    # "render" function takes the template name as its second argument
    # "render" function's third (optional) argument is the context (a way for passing information into the templates aka .html files in the matching names)


def home(request):  
    
    #This function will be run when someone visits the "home" page of the website. 
    #"request" is an object that Django automatically gives you, filled with details about the user's visit
    
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books, 'user': request.user})


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
            try:
                book = self.form.save(user=user, commit=False)
            except openai.InvalidRequestError as e:
                self.form.add_error("gpt_name", f'[API error]\n{e}')
            
            if self.form.is_valid():
                book.save()
                return redirect('home')
            
        return self.render(request)
    
    def get(self, request):
        self.form = NewBookForm()
        return self.render(request)


class UpdateBookView(UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = "update_book.html"
    context_object_name = "book"
    
    def form_valid(self, form):
        book = form.save(self.request.user, commit=False)
        book.updated_by = self.request.user
        book.updated_at = timezone.now()
        book.save()
        return render(self.request, 'update_book.html', {'form': UpdateBookForm(instance=book) })

class DeleteBookView(DeleteView):
    model = Book
    success_url = "/"
    template_name = "delete_book.html"

class BookView(DetailView):
    model = Book
    template_name = "browse_book.html"

class NewChapterView(View):
    def render(self, request, pk):
        return render(request, 'new_chapter.html',
                      {'form': self.form, 'book': Book.objects.get(id=pk)})
    
    def post(self, request, pk):
        user = request.user
        self.form = NewChapterForm(request.POST)
        book = Book.objects.get(id=pk)
        if self.form.is_valid():
            try:
                chapter = self.form.save(user=user, book=book, commit=False)
            except openai.InvalidRequestError as e:
                self.form.add_error("gpt_name", f'[API error]\n{e}')
            
            if self.form.is_valid():
                chapter.save()
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            
        return self.render(request)

    def get(self, request, pk):
        self.form = NewChapterForm()
        return self.render(request, pk)


class DeleteChapterView(DeleteView):
    model = Chapter
    template_name = "delete_chapter.html"

    def get_success_url(self):
        return self.request.POST.get('next', '/')


class UpdateChapterView(UpdateView):
    model = Chapter
    form_class = UpdateChapterForm
    template_name = "update_chapter.html"
    context_object_name = "chapter"
    
    def form_valid(self, form):
        book = Chapter.objects.get(id=self.kwargs["pk"]).book
        chapter = form.save(self.request.user, book, commit=False)
        chapter.updated_by = self.request.user
        chapter.updated_at = timezone.now()
        chapter.save()
        next = self.request.POST.get('next', '/')
        return HttpResponseRedirect(next)
