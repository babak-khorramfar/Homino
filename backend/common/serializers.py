from backend.services import serializers
from common.models import Attachment, City, Region
from django.contrib.contenttypes.models import ContentType


class AttachmentUploadSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()
    object_id = serializers.IntegerField()

    class Meta:
        model = Attachment
        fields = ["file", "content_type", "object_id"]

    def validate_content_type(self, value):
        try:
            ContentType.objects.get(model=value.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("content_type نامعتبر است.")
        return value

    def create(self, validated_data):
        model = validated_data.pop("content_type").lower()
        content_type = ContentType.objects.get(model=model)
        return Attachment.objects.create(content_type=content_type, **validated_data)


class AttachmentListSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "file_url", "uploaded_at"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class CityWithRegionsSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True)

    class Meta:
        model = City
        fields = ["id", "name", "regions"]
