from rest_framework import serializers
from users.models import CustomUser
from services.models import (
    ServiceCategory,
    Service,
    ServiceRequest,
    Proposal,
    OrderStatus,
    Message,
    Report,
    Review,
)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "title"]


class ServiceCategorySerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True)

    class Meta:
        model = ServiceCategory
        fields = ["id", "title", "children"]


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = ["id", "title", "description", "category"]


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ServiceRequest
        fields = ["service_id", "description", "location_text", "scheduled_time"]

    def validate_service_id(self, value):
        from services.models import Service

        if not Service.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("سرویس انتخاب‌شده معتبر نیست.")
        return value

    def create(self, validated_data):
        service_id = validated_data.pop("service_id")
        service = Service.objects.get(id=service_id)
        customer = self.context["request"].user
        return ServiceRequest.objects.create(
            customer=customer, service=service, **validated_data
        )


class ServiceRequestListSerializer(serializers.ModelSerializer):
    service = serializers.StringRelatedField()

    class Meta:
        model = ServiceRequest
        fields = ["id", "service", "status", "description", "created_at"]


class ProposalCreateSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Proposal
        fields = ["request_id", "price", "message"]

    def validate_request_id(self, value):
        try:
            request = ServiceRequest.objects.get(id=value)
        except ServiceRequest.DoesNotExist:
            raise serializers.ValidationError("درخواست مورد نظر وجود ندارد.")
        if request.status != "pending":
            raise serializers.ValidationError(
                "برای این درخواست نمی‌توان پیشنهاد ارسال کرد."
            )
        return value

    def create(self, validated_data):
        request_id = validated_data.pop("request_id")
        service_request = ServiceRequest.objects.get(id=request_id)
        provider = self.context["request"].user
        return Proposal.objects.create(
            request=service_request, provider=provider, **validated_data
        )


class ProposalListSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source="provider.full_name")

    class Meta:
        model = Proposal
        fields = ["id", "provider", "price", "message", "created_at"]


class OrderStatusUpdateSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    new_status = serializers.ChoiceField(
        choices=[status[0] for status in OrderStatus.STATUS_CHOICES]
    )
    note = serializers.CharField(allow_blank=True, required=False)


class OrderStatusDetailSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source="provider.full_name")

    class Meta:
        model = OrderStatus
        fields = [
            "request_id",
            "current_status",
            "note",
            "started_at",
            "finished_at",
            "canceled_at",
            "provider",
        ]


class MessageCreateSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ["request_id", "receiver_id", "content"]

    def validate(self, data):
        from services.models import ServiceRequest

        try:
            request_obj = ServiceRequest.objects.get(id=data["request_id"])
        except ServiceRequest.DoesNotExist:
            raise serializers.ValidationError("درخواست مورد نظر یافت نشد.")

        if data["receiver_id"] == self.context["request"].user.id:
            raise serializers.ValidationError("گیرنده نمی‌توانید خودتان باشید.")

        try:
            receiver = CustomUser.objects.get(id=data["receiver_id"])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("گیرنده یافت نشد.")

        return data

    def create(self, validated_data):
        return Message.objects.create(
            sender=self.context["request"].user,
            receiver_id=validated_data["receiver_id"],
            request_id=validated_data["request_id"],
            content=validated_data["content"],
        )


class MessageListSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.full_name")
    receiver = serializers.CharField(source="receiver.full_name")

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "created_at"]


class ReportCreateSerializer(serializers.ModelSerializer):
    reported_user_id = serializers.IntegerField(required=False)
    request_id = serializers.IntegerField(required=False)

    class Meta:
        model = Report
        fields = ["report_type", "reported_user_id", "request_id", "message"]

    def validate(self, data):
        if not data.get("reported_user_id") and not data.get("request_id"):
            raise serializers.ValidationError(
                "باید حداقل یکی از فیلدهای reported_user_id یا request_id را وارد کنید."
            )
        return data

    def create(self, validated_data):
        reporter = self.context["request"].user
        report = Report.objects.create(
            reporter=reporter,
            report_type=validated_data["report_type"],
            message=validated_data["message"],
            reported_user_id=validated_data.get("reported_user_id"),
            request_id=validated_data.get("request_id"),
        )
        return report


class ReportListSerializer(serializers.ModelSerializer):
    reporter = serializers.CharField(source="reporter.full_name")
    reported_user = serializers.CharField(
        source="reported_user.full_name", default=None
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "report_type",
            "message",
            "reporter",
            "reported_user",
            "request_id",
            "created_at",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ["request_id", "punctuality", "behavior", "quality", "comment"]

    def validate_request_id(self, value):
        try:
            request = ServiceRequest.objects.get(id=value)
        except ServiceRequest.DoesNotExist:
            raise serializers.ValidationError("درخواست یافت نشد.")
        if request.review:
            raise serializers.ValidationError(
                "برای این سفارش قبلاً بازخورد ثبت شده است."
            )
        if request.status != "finished":
            raise serializers.ValidationError(
                "فقط پس از اتمام سفارش می‌توان نظر ثبت کرد."
            )
        return value

    def create(self, validated_data):
        service_request = ServiceRequest.objects.get(id=validated_data["request_id"])
        return Review.objects.create(
            request=service_request,
            customer=service_request.customer,
            provider=service_request.order_status.provider,
            punctuality=validated_data["punctuality"],
            behavior=validated_data["behavior"],
            quality=validated_data["quality"],
            comment=validated_data["comment"],
        )


class ReviewListItemSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source="customer.full_name")

    class Meta:
        model = Review
        fields = [
            "customer",
            "comment",
            "punctuality",
            "behavior",
            "quality",
            "created_at",
        ]
