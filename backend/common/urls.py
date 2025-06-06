from django.urls import path
from common.api_views import AttachmentUploadView

urlpatterns = [
    path(
        "attachment/upload/", AttachmentUploadView.as_view(), name="upload-attachment"
    ),
]
