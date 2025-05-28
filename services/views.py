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


@login_required
def create_service_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect("home")  # یا هر صفحه‌ای که بعد از ثبت می‌خوای نمایش بدی
    else:
        form = ServiceRequestForm()

    return render(request, "services/create_request.html", {"form": form})
