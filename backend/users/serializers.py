from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from services.models import Service
from users.models import (
    CustomUser,
    CustomerProfile,
    ProviderProfile,
    CustomerProfile,
    ProviderProfile,
)


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


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data["phone"], password=data["password"])
        if not user:
            raise serializers.ValidationError("شماره یا رمز عبور نادرست است.")
        if not user.is_active:
            raise serializers.ValidationError("حساب شما غیرفعال است.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
            "full_name": user.full_name,
        }


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["address", "city", "profile_image"]

    def validate_profile_image(self, image):
        max_size = 3 * 1024 * 1024  # ۳ مگابایت
        allowed_types = ["image/jpeg", "image/png"]

        if image.size > max_size:
            raise serializers.ValidationError(
                "حجم تصویر نباید بیشتر از ۳ مگابایت باشد."
            )

        if image.content_type not in allowed_types:
            raise serializers.ValidationError("فقط فرمت‌های jpg و png مجاز هستند.")

        return image


class ProviderProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ["bio", "profile_image", "is_available"]

    def validate_profile_image(self, image):
        max_size = 3 * 1024 * 1024  # ۳ مگابایت
        allowed_types = ["image/jpeg", "image/png"]

        if image.size > max_size:
            raise serializers.ValidationError(
                "حجم تصویر نباید بیشتر از ۳ مگابایت باشد."
            )

        if image.content_type not in allowed_types:
            raise serializers.ValidationError("فقط فرمت‌های jpg و png مجاز هستند.")

        return image


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title"]


class SkillUpdateSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate_skills(self, skill_ids):
        from services.models import Service

        valid_ids = set(
            Service.objects.filter(id__in=skill_ids).values_list("id", flat=True)
        )
        invalid_ids = set(skill_ids) - valid_ids
        if invalid_ids:
            raise serializers.ValidationError(f"شناسه‌های نامعتبر: {list(invalid_ids)}")
        return skill_ids
