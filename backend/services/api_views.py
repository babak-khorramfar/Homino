from rest_framework.views import APIView
from rest_framework.response import Response
from services.models import ServiceCategory, Service
from users.permissions import IsCustomer
from rest_framework.permissions import IsAuthenticated
from services.serializers import (
    ServiceCategorySerializer,
    ServiceSerializer,
    ServiceRequestCreateSerializer,
    ServiceRequestListSerializer,
)
from rest_framework import generics


class CategoryListView(APIView):
    def get(self, request):
        parents = ServiceCategory.objects.filter(parent__isnull=True)
        serializer = ServiceCategorySerializer(parents, many=True)
        return Response(serializer.data)


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ServiceRequestCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = ServiceRequestCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "درخواست با موفقیت ثبت شد."}, status=201)
        return Response(serializer.errors, status=400)


class MyServiceRequestsView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        requests = request.user.service_requests.all().order_by("-created_at")
        serializer = ServiceRequestListSerializer(requests, many=True)
        return Response(serializer.data)
