from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import (
    UserProfile,
    ServiceRequest,
    Proposal,
    Review,
    ChatMessage,
    SupportTicket,
)


class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ("customer", _("Customer")),
        ("provider", _("Service Provider")),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label=_("User Type"))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "user_type"]
        labels = {
            "username": _("Username"),
            "email": _("Email"),
            "password1": _("Password"),
            "password2": _("Confirm Password"),
            "user_type": _("User Type"),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.user_type = self.cleaned_data["user_type"]
            user_profile.save()
        return user


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["category", "city", "address", "description"]
        labels = {
            "category": _("Service Category"),
            "city": _("City"),
            "address": _("Address"),
            "description": _("Description"),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ["price_estimate", "message"]
        labels = {
            "price_estimate": _("Estimated Price"),
            "message": _("Message"),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, label=_("Rating"), widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        labels = {
            "comment": _("Comment"),
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["message"]
        labels = {
            "message": _("Message"),
        }


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["subject", "message"]
        labels = {
            "subject": _("Subject"),
            "message": _("Message"),
        }
