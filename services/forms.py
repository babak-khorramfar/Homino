from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, ServiceRequest


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
