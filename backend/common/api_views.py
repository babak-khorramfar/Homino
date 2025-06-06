from common.serializers import (
    AttachmentUploadSerializer,
    AttachmentListSerializer,
    CityWithRegionsSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from common.models import Attachment, City
from django.http import FileResponse, Http404


class AttachmentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = AttachmentUploadSerializer(data=request.data)
        if serializer.is_valid():
            attachment = serializer.save()
            return Response(
                {
                    "id": attachment.id,
                    "file_url": attachment.file.url,
                    "created_at": attachment.uploaded_at,
                },
                status=201,
            )
        return Response(serializer.errors, status=400)


class AttachmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_type_str = request.query_params.get("content_type")
        object_id = request.query_params.get("object_id")

        if not content_type_str or not object_id:
            return Response(
                {"error": "پارامترهای content_type و object_id الزامی هستند."},
                status=400,
            )

        try:
            model = ContentType.objects.get(model=content_type_str.lower())
        except ContentType.DoesNotExist:
            return Response({"error": "content_type نامعتبر است."}, status=400)

        attachments = Attachment.objects.select_related("content_type").filter(
            content_type=model, object_id=object_id
        )
        serializer = AttachmentListSerializer(
            attachments, many=True, context={"request": request}
        )
        return Response(serializer.data)


class AttachmentDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, attachment_id):
        try:
            attachment = Attachment.objects.select_related("content_type").get(
                id=attachment_id
            )
        except Attachment.DoesNotExist:
            raise Http404("فایل پیدا نشد.")

        # مدل مرتبط رو واکشی می‌کنیم
        linked_model = attachment.content_type.model_class()
        obj = linked_model.objects.filter(id=attachment.object_id).first()

        # بررسی دسترسی
        user = request.user
        has_access = False

        if hasattr(obj, "customer") and obj.customer == user:
            has_access = True
        elif hasattr(obj, "provider") and obj.provider == user:
            has_access = True
        elif hasattr(obj, "sender") and obj.sender == user:
            has_access = True
        elif hasattr(obj, "receiver") and obj.receiver == user:
            has_access = True
        elif user.is_staff or user.is_superuser:
            has_access = True

        if not has_access:
            return Response({"error": "شما به این فایل دسترسی ندارید."}, status=403)

        return FileResponse(attachment.file, filename=attachment.file.name)


class CityRegionListView(APIView):
    def get(self, request):
        cities = City.objects.prefetch_related("regions").all()
        serializer = CityWithRegionsSerializer(cities, many=True)
        return Response(serializer.data)
