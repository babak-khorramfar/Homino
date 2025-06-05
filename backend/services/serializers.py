from rest_framework import serializers
from services.models import ServiceCategory, Service


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
