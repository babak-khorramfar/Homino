from django.urls import path
from common.api_views import (
    AttachmentDownloadView,
    AttachmentListView,
    AttachmentUploadView,
    CityRegionListView,
)

urlpatterns = [
    path(
        "attachment/upload/", AttachmentUploadView.as_view(), name="upload-attachment"
    ),
    path("attachments/", AttachmentListView.as_view(), name="attachment-list"),
    path("locations/", CityRegionListView.as_view(), name="city-region-list"),
    path(
        "attachment/download/<int:attachment_id>/",
        AttachmentDownloadView.as_view(),
        name="download-attachment",
    ),
]
