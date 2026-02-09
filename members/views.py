from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError

from .models import User

# Create your views here.
def index(request):
    return render(request, "members/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.Post['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "members/login.html", {
                "message": "Invalid username and/ or password"
            })
    else:
        return render(request, "members/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request["confirm_password"]

        if password != confirm_password:
            return render(request, "members/register.html", {
                "message": "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "members/register.html",{
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(render(reverse("index")))