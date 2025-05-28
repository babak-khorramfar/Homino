from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .forms import ServiceRequestForm
from django.contrib.auth.decorators import login_required


def home(request):
    return HttpResponse("Welcome to Homino! 😎")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # آدرس صفحه لاگین (یا داشبورد)
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def service_list(request):
    return HttpResponse("Service list is working.")
