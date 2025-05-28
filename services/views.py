from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ServiceCategory
from .models import ServiceRequest


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
    categories = ServiceCategory.objects.all()
    return render(request, "services/service_list.html", {"categories": categories})


def request_list(request):
    requests = ServiceRequest.objects.all().order_by("-created_at")
    return render(request, "services/request_list.html", {"requests": requests})
