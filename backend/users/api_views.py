from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models.user import CustomUser
from users.serializers import (
    SignupSerializer,
    LoginSerializer,
    CustomerProfileUpdateSerializer,
    ProviderProfileUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsCustomer, IsProvider
from common.models import ActivityLog


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "ثبت‌نام با موفقیت انجام شد."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(phone=request.data["phone"])
            ActivityLog.objects.create(user=user, action="login")
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ActivityLog.objects.create(user=request.user, action="logout")
        return Response({"message": "خروج با موفقیت ثبت شد."}, status=200)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "phone": user.phone,
            "full_name": user.full_name,
            "role": user.role,
        }

        if user.role == "customer" and hasattr(user, "customer_profile"):
            data["profile"] = {
                "address": user.customer_profile.address,
                "city": user.customer_profile.city,
            }

        elif user.role == "provider" and hasattr(user, "provider_profile"):
            data["profile"] = {
                "bio": user.provider_profile.bio,
                "is_verified": user.provider_profile.is_verified,
                "is_available": user.provider_profile.is_available,
            }

        return Response(data)


class UpdateCustomerProfileView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def put(self, request):
        user = request.user
        if user.role != "customer" or not hasattr(user, "customer_profile"):
            raise PermissionDenied("شما مجاز به بروزرسانی این پروفایل نیستید.")

        profile = user.customer_profile
        serializer = CustomerProfileUpdateSerializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "پروفایل با موفقیت بروزرسانی شد."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProviderProfileView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def put(self, request):
        user = request.user
        if user.role != "provider" or not hasattr(user, "provider_profile"):
            raise PermissionDenied("شما مجاز به بروزرسانی این پروفایل نیستید.")

        profile = user.provider_profile
        serializer = ProviderProfileUpdateSerializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "پروفایل با موفقیت بروزرسانی شد."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
