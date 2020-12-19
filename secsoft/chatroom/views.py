from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

def loginPage(request):
  return render(request, 'login.html')
