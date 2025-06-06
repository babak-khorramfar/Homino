from datetime import timezone
from rest_framework.views import APIView
from django.db.models import Avg
from rest_framework.response import Response
from services.models import (
    ServiceCategory,
    Service,
    Proposal,
    OrderStatus,
    ServiceRequest,
    Report,
)
from users.permissions import IsCustomer, IsProvider, IsAdminOrSupport
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from services.serializers import (
    MessageCreateSerializer,
    MessageListSerializer,
    OrderStatusDetailSerializer,
    ReportCreateSerializer,
    ReviewCreateSerializer,
    ReviewListItemSerializer,
    ServiceCategorySerializer,
    ServiceSerializer,
    ServiceRequestCreateSerializer,
    ServiceRequestListSerializer,
    ProposalCreateSerializer,
    ProposalListSerializer,
    OrderStatusUpdateSerializer,
    ReportListSerializer,
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


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    def post(self, request):
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                status_obj = OrderStatus.objects.get(
                    request_id=data["request_id"], provider=request.user
                )
            except OrderStatus.DoesNotExist:
                return Response(
                    {"error": "شما دسترسی به این سفارش ندارید یا وضعیت موجود نیست."},
                    status=404,
                )

            status_obj.current_status = data["new_status"]
            status_obj.note = data.get("note", "")
            if data["new_status"] == "started":
                status_obj.started_at = timezone.now()
            elif data["new_status"] == "finished":
                status_obj.finished_at = timezone.now()
            elif data["new_status"] == "canceled":
                status_obj.canceled_at = timezone.now()
            status_obj.save()

            return Response({"message": "وضعیت سفارش بروزرسانی شد."}, status=200)

        return Response(serializer.errors, status=400)


class OrderStatusDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        try:
            status = OrderStatus.objects.get(request_id=request_id)
        except OrderStatus.DoesNotExist:
            return Response({"error": "اطلاعات وضعیت سفارش یافت نشد."}, status=404)

        user = request.user
        if status.provider != user and status.request.customer != user:
            return Response(
                {"error": "شما مجاز به مشاهده این سفارش نیستید."}, status=403
            )

        serializer = OrderStatusDetailSerializer(status)
        return Response(serializer.data)


class ScheduledTimeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        try:
            service_request = ServiceRequest.objects.get(id=request_id)
        except ServiceRequest.DoesNotExist:
            return Response({"error": "درخواست مورد نظر یافت نشد."}, status=404)

        # فقط مشتری یا متخصص همان سفارش مجاز هستند
        if service_request.customer != request.user and not hasattr(
            request.user, "provider_profile"
        ):
            return Response(
                {"error": "شما مجاز به مشاهده این سفارش نیستید."}, status=403
            )

        return Response(
            {
                "request_id": service_request.id,
                "scheduled_time": service_request.scheduled_time,
            }
        )


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "پیام با موفقیت ارسال شد."}, status=201)
        return Response(serializer.errors, status=400)


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        from services.models import ServiceRequest

        try:
            service_request = ServiceRequest.objects.get(id=request_id)
        except ServiceRequest.DoesNotExist:
            return Response({"error": "سفارش مورد نظر یافت نشد."}, status=404)

        if service_request.customer != request.user and not hasattr(
            request.user, "provider_profile"
        ):
            return Response({"error": "شما به این مکالمه دسترسی ندارید."}, status=403)

        messages = service_request.messages.all().order_by("created_at")
        serializer = MessageListSerializer(messages, many=True)
        return Response(serializer.data)


class ReportCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "گزارش با موفقیت ثبت شد."}, status=201)
        return Response(serializer.errors, status=400)


class ReportListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSupport]

    def get(self, request):
        reports = Report.objects.all().order_by("-created_at")
        serializer = ReportListSerializer(reports, many=True)
        return Response(serializer.data)


class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "نظر شما ثبت شد."}, status=201)
        return Response(serializer.errors, status=400)


class ProviderReviewStatsView(APIView):
    def get(self, request, provider_id):
        try:
            provider = CustomUser.objects.get(id=provider_id, role="provider")
        except CustomUser.DoesNotExist:
            return Response({"error": "متخصص مورد نظر یافت نشد."}, status=404)

        reviews = provider.received_reviews.all()
        stats = reviews.aggregate(
            avg_punctuality=Avg("punctuality"),
            avg_behavior=Avg("behavior"),
            avg_quality=Avg("quality"),
        )

        total_avg = (
            round(
                (
                    (stats["avg_punctuality"] or 0)
                    + (stats["avg_behavior"] or 0)
                    + (stats["avg_quality"] or 0)
                )
                / 3,
                2,
            )
            if reviews.exists()
            else 0
        )

        serializer = ReviewListItemSerializer(reviews, many=True)

        return Response(
            {
                "provider_id": provider.id,
                "average_punctuality": round(stats["avg_punctuality"] or 0, 2),
                "average_behavior": round(stats["avg_behavior"] or 0, 2),
                "average_quality": round(stats["avg_quality"] or 0, 2),
                "average_total": total_avg,
                "reviews": serializer.data,
            }
        )
