from django.shortcuts import render

def index(request):
    return render(
        request,'default.html'
    )

def about(request):
    return render(
        request,'about_page.html'
    )

def contacts(request):
    return render(
        request,'contact_page.html'
    )