from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages

from .forms import SearchForm
from .models import Search


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search']
            form.save()
            form.slug = text
            args = {'form': form, 'text':text}       
            return render(request, 'scrapy/results.html', args)

    form = SearchForm()
    return render(request, 'main/home.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"Your are logged in as {username}")
            return redirect("main:home")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, "main/register.html", {"form": form})

    form = UserCreationForm
    return render(request, "main/register.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out Successfully!")
    return redirect("main:home")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are successfully logged in as {username}!")
                return redirect("main:home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})





