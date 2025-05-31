from django.shortcuts import render, redirect
from .forms import CustomUser
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
from .models import Proposal, Review, ChatMessage, SupportTicket
from .forms import ProposalForm, ReviewForm, ChatMessageForm, SupportTicketForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def splash_view(request):
    return render(request, "splash.html")


def home(request):
    categories = ServiceCategory.objects.filter(parent__isnull=True).prefetch_related(
        "children"
    )
    return render(request, "services/customer/home.html", {"categories": categories})


def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match"})

        user = CustomUser.objects.create_user(
            full_name=full_name,
            phone=phone,
            password=password1,
        )

        # به‌روزرسانی نقش در UserProfile
        profile = user.profile
        profile.user_type = role
        profile.save()

        login(request, user)  # ورود خودکار
        return redirect("home")  # ریدایرکت به صفحه اصلی

    return render(request, "registration/register.html")


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


@role_required("provider")
def create_proposal(request, request_id):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)
    if request.method == "POST":
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.provider = request.user
            proposal.service_request = service_request
            proposal.save()
            return redirect("request_list")
    else:
        form = ProposalForm()
    return render(
        request,
        "services/proposal_form.html",
        {"form": form, "request": service_request},
    )


@role_required("customer")
def create_review(request, request_id):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.service_request = service_request
            review.provider = (
                service_request.proposals.filter(is_accepted=True).first().provider
            )
            review.save()
            return redirect("request_list")
    else:
        form = ReviewForm()
    return render(request, "services/review_form.html", {"form": form})


@login_required
def send_message(request, receiver_id):
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver_id = receiver_id
            message.save()
            return redirect("home")  # یا به صفحه گفت‌و‌گو
    else:
        form = ChatMessageForm()
    return render(request, "services/chat_form.html", {"form": form})


@login_required
def submit_ticket(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("support_thank_you")  # یا صفحه تیکت‌ها
    else:
        form = SupportTicketForm()
    return render(request, "support/ticket_form.html", {"form": form})
