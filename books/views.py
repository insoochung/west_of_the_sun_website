from django.shortcuts import render

def home(request):
    return render.HttpResponse('Hello, World!')
