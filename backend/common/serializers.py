from backend.services import serializers
from common.models import Attachment
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
