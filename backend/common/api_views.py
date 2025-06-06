from common.serializers import AttachmentUploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
