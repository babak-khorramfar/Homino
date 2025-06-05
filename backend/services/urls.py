from django.urls import path
from .views import (
    splash_view,
    home,
    service_list,
    request_list,
    create_service_request,
    create_proposal,
    create_review,
    send_message,
    submit_ticket,
)
from .api_views import (
    ServiceRequestCreateAPI,
    ProposalCreateAPI,
    ReviewCreateAPI,
    ChatMessageCreateAPI,
    SupportTicketCreateAPI,
)

urlpatterns = [
    path("", splash_view, name="splash"),  # splash screen
    path("splash/", splash_view),
    path("home/", home, name="home"),
    # CUSTOMER
    path("categories/", service_list, name="service_list"),
    path("requests/", request_list, name="request_list"),
    path("requests/new/", create_service_request, name="create_service_request"),
    path("requests/<int:request_id>/review/", create_review, name="create_review"),
    # PROVIDER
    path("requests/<int:request_id>/propose/", create_proposal, name="create_proposal"),
    # MESSAGES
    path("messages/send/<int:receiver_id>/", send_message, name="send_message"),
    # SUPPORT
    path("support/ticket/", submit_ticket, name="submit_ticket"),
    path("requests/", ServiceRequestCreateAPI.as_view(), name="api_create_request"),
    path(
        "requests/<int:request_id>/propose/",
        ProposalCreateAPI.as_view(),
        name="api_create_proposal",
    ),
    path(
        "requests/<int:request_id>/review/",
        ReviewCreateAPI.as_view(),
        name="api_create_review",
    ),
    path(
        "messages/send/<int:receiver_id>/",
        ChatMessageCreateAPI.as_view(),
        name="api_send_message",
    ),
    path("support/ticket/", SupportTicketCreateAPI.as_view(), name="api_submit_ticket"),
]
