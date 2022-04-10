from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
import time

# Create your views here.

def homepage(request):
    return render(request,'members/index.html') # va pas renvoyer juste 1 element mais renvoie la page entiere

def canvas(request):
    if request.user.is_authenticated:
        return render(request,'members/canvas.html')
    else:
        return redirect('/login/')
