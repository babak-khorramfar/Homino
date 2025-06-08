from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import (
    SignupSerializer,
    LoginSerializer,
    CustomerProfileUpdateSerializer,
    ProviderProfileUpdateSerializer,
    SkillSerializer,
    SkillUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsCustomer, IsProvider
from common.models import ActivityLog, CustomUser, CustomerProfile, ProviderProfile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)


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


class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"detail": "شماره تلفن الزامی است."}, status=400)

        # ساخت کد تأیید تستی (در آینده واقعی)
        code = "123456"

        # ذخیره موقتی در session (فعلاً ساده)
        request.session[f"otp_{phone}"] = code

        return Response({"message": "کد تأیید ارسال شد."}, status=200)


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("otp")
        role = request.data.get("role")  # فقط برای ثبت‌نام

        if not phone or not code:
            return Response({"detail": "شماره یا کد ناقص است."}, status=400)

        session_code = request.session.get(f"otp_{phone}")
        if session_code != code:
            return Response({"detail": "کد تأیید نادرست است."}, status=400)

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            if not role:
                return Response(
                    {"detail": "کاربر جدید است. انتخاب نقش الزامی است."}, status=400
                )

            user = CustomUser.objects.create(
                phone=phone, full_name="کاربر جدید", role=role
            )
            user.set_unusable_password()
            user.save()

            if role == "customer":
                CustomerProfile.objects.create(user=user)
            elif role == "provider":
                ProviderProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
            },
            status=200,
        )


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


class ProviderSkillListView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def get(self, request):
        user = request.user
        skills = user.provider_profile.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"skills": serializer.data})


from users.serializers import SkillUpdateSerializer
from services.models import Service


class ProviderSkillUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def put(self, request):
        serializer = SkillUpdateSerializer(data=request.data)
        if serializer.is_valid():
            skill_ids = serializer.validated_data["skills"]
            request.user.provider_profile.skills.set(
                Service.objects.filter(id__in=skill_ids)
            )
            return Response({"message": "مهارت‌ها با موفقیت بروزرسانی شدند."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutRealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "خروج با موفقیت انجام شد."}, status=200)
        except Exception as e:
            return Response({"error": "توکن معتبر نیست یا قبلاً باطل شده."}, status=400)
