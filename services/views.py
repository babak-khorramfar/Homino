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
from django.contrib import messages
from django.contrib.auth import authenticate, login


def splash_view(request):
    return render(request, "splash.html")


def home(request):
    categories = ServiceCategory.objects.filter(parent__isnull=True).prefetch_related(
        "children"
    )
    return render(request, "services/customer/home.html", {"categories": categories})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")  # جلوگیری از دسترسی مجدد
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


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        phone = request.POST.get("username")
        password = request.POST.get("password")
        otp = request.POST.get("otp")

        user = authenticate(request, username=phone, password=password)

        if user is not None:
            if otp == "123456" or not otp:
                if otp:  # اگر otp وارد شده، یعنی فاز تأیید نهایی
                    login(request, user)
                    return redirect("home")
                else:
                    # فاز اول لاگین موفق، نمایش فرم OTP
                    messages.info(
                        request, _("Verification code sent (test mode: 123456)")
                    )
            else:
                messages.error(request, _("Invalid verification code."))
        else:
            messages.error(request, _("Invalid phone number or password."))

    return render(request, "registration/login.html")
