from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404 # for returning rendered templates ASAP
from .models import Book, Chapter, Content
from django.http import HttpResponse # for testing only, delete later

    # "render" function takes the request object as its first argument
    # "render" function takes the template name as its second argument
    # "render" function's third (optional) argument is the context (a way for passing information into the templates aka .html files in the matching names)

    
def home(request):  
    
    #This function will be run when someone visits the "home" page of the website. 
    #"request" is an object that Django automatically gives you, filled with details about the user's visit
    
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

def book_chapters(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'chapters.html', {'book': book})

def about(request):
    #return HttpResponse('<h1> About View Test </h1>') # for testing
    return render(request, 'about.html')

def about_company(request):
    #return HttpResponse('<h1> About Company View Test </h1>') # for testing
    return render(request, 'about_company.html', {'company_name': 'West of the Sun'})

def user_profile(request):
    #return HttpResponse('<h1> User Profile Page Test </h1>') # for testing
    return render(request, 'user_profile.html,')

def new_chapter(request, id):
    book = get_object_or_404(Book, id=id)

    # POST method is used when one wants to change data on the server
    # Django protects all POST requests using a CSRF Token
    # Every time the application receives a POST, it will first look for the CSRF Token. 
    # If the request has no token, or the token is invalid, it will discard the posted data.

    # Check new_chapter.html for reference
    if request.method == 'POST' :
        title = request.POST['title']
        content_prompt = request.POST['content_prompt']

        user = User.objects.first() # TODO: get the currently logged in user

        chapter = Chapter.objects.create(
            title = title,
            book = book,
            created_by = user,
            content_prompt = content_prompt
        )

        content = Content.objects.create(

                chapter = chapter,
                created_by = user
        )

        return redirect ('book_chapters', id=book.id)   # TODO: redirect to the created topic page
