from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import ServiceCategory
from .models import ServiceRequest
from .forms import ServiceRequestForm
from services.decorators import role_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import UserProfile


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


class CustomLoginView(LoginView):
    def get_success_url(self):
        profile = self.request.user.profile
        if profile.user_type == UserProfile.UserType.CUSTOMER:
            return reverse("service_list")  # یا هر آدرس مناسب برای مشتری
        elif profile.user_type == UserProfile.UserType.PROVIDER:
            return reverse("request_list")  # یا صفحه سفارش‌های مرتبط با تخصص متخصص
        return reverse("home")  # fallback


@role_required("customer")
def service_list(request):
    categories = ServiceCategory.objects.all()
    return render(request, "services/service_list.html", {"categories": categories})


@role_required("provider")
def request_list(request):
    user = request.user
    requests = ServiceRequest.objects.filter(customer=user)
    return render(request, "services/request_list.html", {"requests": requests})


@role_required("provider")
def request_create(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect("request_list")
    else:
        form = ServiceRequestForm()
    return render(request, "services/request_form.html", {"form": form})


@role_required("customer")
def create_service_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect("request_list")
    else:
        form = ServiceRequestForm()
    return render(request, "services/create_request.html", {"form": form})
