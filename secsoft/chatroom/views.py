from pathlib import Path
import sqlite3

from django.http.response import JsonResponse
from chatroom.models import Post
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

@login_required
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

    

class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html', {'form':  AuthenticationForm})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        ## The developer forgot to remove debugging code from production
        ## This leaks passwords and user information to console
        print("username: " + request.POST.get('username'))
        print("password: " + request.POST.get('password'))
        
        if form.is_valid():


            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return HttpResponseRedirect(reverse_lazy('adopcion:solicitud_listar'))


            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'login.html',
                    {'form': AuthenticationForm, 'invalid_creds': True}
                )

            login(request, user)

            return redirect(reverse('index'))


class RegisterPage(View):
    def get(self, request):
        return render(request, 'signup.html', {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'signup.html', {'form': form})

## This allows attacker to post messages without authorization (can be fixed with login required annotation)
def postMessage(request):
    ## This is part of the XSS attack, to make things even worse, the executable code is also saved to database
    Post.objects.create(content=request.POST.get('content'))
    return redirect('/')

## Endpoint that allows SQL injections
def findById(request):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    ## Using executescript and unsantized inputs makes this easy to exploit
    print("SELECT * FROM chatroom_post WHERE id = %s%%;" % (request.GET.get('id').replace("%20", " ")))
    res = cursor.executescript("SELECT * FROM chatroom_post WHERE id = '%s%%';" % (request.GET.get('id').replace("%20", " "))).fetchall()
    return JsonResponse({'posts': res})

    