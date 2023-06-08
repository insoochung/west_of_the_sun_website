from django.shortcuts import redirect, render, get_object_or_404 # for returning rendered templates ASAP

from .models import Book
from .forms import NewBookForm
from .gpt_calls import call_gpt

    # "render" function takes the request object as its first argument
    # "render" function takes the template name as its second argument
    # "render" function's third (optional) argument is the context (a way for passing information into the templates aka .html files in the matching names)

    
def home(request):  
    
    #This function will be run when someone visits the "home" page of the website. 
    #"request" is an object that Django automatically gives you, filled with details about the user's visit
    
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books, 'user': request.user})

def new_book(request):
    user = request.user
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.description = call_gpt(system_prompt=book.meta_prompt,
                                        conv_init_role="user",
                                        dialog=[book.initial_prompt],
                                        model=book.gpt_name,
                                        message_only=True)
            book.created_by = user
            book.save()
            return redirect('home')
    else:
        form = NewBookForm()
    return render(request, 'new_book.html', {'form': form})

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