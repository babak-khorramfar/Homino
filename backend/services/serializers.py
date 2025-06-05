from rest_framework import serializers
from services.models import ServiceCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "title"]


class ServiceCategorySerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True)

    class Meta:
        model = ServiceCategory
        fields = ["id", "title", "children"]
