from django.urls import path
from common.api_views import AttachmentListView, AttachmentUploadView

urlpatterns = [
    path(
        "attachment/upload/", AttachmentUploadView.as_view(), name="upload-attachment"
    ),
    path("attachments/", AttachmentListView.as_view(), name="attachment-list"),
]
