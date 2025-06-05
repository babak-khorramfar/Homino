from rest_framework.views import APIView
from rest_framework.response import Response
from services.models import ServiceCategory, Service, Proposal, ServiceRequest
from users.permissions import IsCustomer, IsProvider
from rest_framework.permissions import IsAuthenticated
from services.serializers import (
    ServiceCategorySerializer,
    ServiceSerializer,
    ServiceRequestCreateSerializer,
    ServiceRequestListSerializer,
    ProposalCreateSerializer,
    ProposalListSerializer,
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


class ProposalCreateView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def post(self, request):
        serializer = ProposalCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "پیشنهاد با موفقیت ارسال شد."}, status=201)
        return Response(serializer.errors, status=400)


class RequestProposalsView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, request_id):
        try:
            service_request = request.user.service_requests.get(id=request_id)
        except:
            return Response({"error": "دسترسی غیرمجاز یا سفارش یافت نشد."}, status=404)

        proposals = service_request.proposals.all().order_by("-created_at")
        serializer = ProposalListSerializer(proposals, many=True)
        return Response(serializer.data)


class AcceptProposalView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        proposal_id = request.data.get("proposal_id")
        try:
            proposal = Proposal.objects.get(id=proposal_id)
        except Proposal.DoesNotExist:
            return Response({"error": "پیشنهاد یافت نشد."}, status=404)

        service_request = proposal.request
        if service_request.customer != request.user:
            return Response({"error": "شما مالک این سفارش نیستید."}, status=403)
        if service_request.status != "pending":
            return Response({"error": "امکان تأیید پیشنهاد وجود ندارد."}, status=400)

        # تغییر وضعیت سفارش
        service_request.status = "accepted"
        service_request.save()

        # وضعیت پیشنهاد انتخاب‌شده
        proposal.status = "accepted"
        proposal.save()

        # رد کردن سایر پیشنهادها
        Proposal.objects.filter(request=service_request).exclude(id=proposal_id).update(
            status="rejected"
        )

        return Response({"message": "پیشنهاد با موفقیت تأیید شد."}, status=200)
