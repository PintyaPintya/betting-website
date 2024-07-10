from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User

# Create your views here.

def index(request):
    return render(request, "betlord/index.html")

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "betlord/register.html", {
                "message": "Passwords must match"
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "betlord/register.html", {
                "message": "Username already taken"
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "betlord/register.html")


def login_view(request):
    if request.method == 'POST':

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "betlord/login.html", {
                "message": "Invalid username and/or password"
            })
    
    else:
        return render(request, "betlord/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))