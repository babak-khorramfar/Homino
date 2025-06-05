from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import SignupSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated


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
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
