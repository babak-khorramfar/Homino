from rest_framework import serializers
from users.models import CustomUser, CustomerProfile, ProviderProfile


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ["phone", "full_name", "role", "password"]

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        user = CustomUser.objects.create(role=role, **validated_data)
        user.set_password(password)
        user.save()

        # ایجاد پروفایل مرتبط
        if role == "customer":
            CustomerProfile.objects.create(user=user)
        elif role == "provider":
            ProviderProfile.objects.create(user=user)

        return user
