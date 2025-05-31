from django.urls import path
from . import api_views

urlpatterns = [
    path(
        "requests/",
        api_views.ServiceRequestCreateAPI.as_view(),
        name="api_request_create",
    ),
    path(
        "proposals/", api_views.ProposalCreateAPI.as_view(), name="api_proposal_create"
    ),
    path("reviews/", api_views.ReviewCreateAPI.as_view(), name="api_review_create"),
    path(
        "messages/", api_views.ChatMessageCreateAPI.as_view(), name="api_message_create"
    ),
    path(
        "support/",
        api_views.SupportTicketCreateAPI.as_view(),
        name="api_support_create",
    ),
]
