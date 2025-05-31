from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import (
    CustomUser,
    UserProfile,
    ServiceRequest,
    Proposal,
    Review,
    ChatMessage,
    SupportTicket,
)


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(label=_("Full Name"), max_length=255)
    phone = forms.CharField(label=_("Phone Number"), max_length=20)
    user_type = forms.ChoiceField(
        label=_("User Type"),
        choices=UserProfile.UserType.choices,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = CustomUser
        fields = ["phone", "full_name", "password1", "password2", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data["phone"]
        user.full_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user, defaults={"user_type": self.cleaned_data["user_type"]}
            )
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
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        labels = {
            "rating": _("Rating"),
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
