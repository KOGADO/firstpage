from django.shortcuts import render

def home_view(request):
    return render(request, 'dobje/home.html')

def info_view(request):
    return render(request, 'dobje/info.html')