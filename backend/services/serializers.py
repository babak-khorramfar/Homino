from rest_framework import serializers
from services.models import ServiceCategory, Service, ServiceRequest


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
