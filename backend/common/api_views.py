from common.serializers import AttachmentUploadSerializer, AttachmentListSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from common.models import Attachment


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

        attachments = Attachment.objects.filter(content_type=model, object_id=object_id)
        serializer = AttachmentListSerializer(
            attachments, many=True, context={"request": request}
        )
        return Response(serializer.data)
