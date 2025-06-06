from django.urls import path
from services.api_views import (
    CategoryListView,
    CreateReviewView,
    MessageListView,
    OrderStatusDetailView,
    ProviderReviewStatsView,
    ReportCreateView,
    ReportListView,
    ScheduledTimeView,
    SendMessageView,
    ServiceListView,
    ServiceRequestCreateView,
    MyServiceRequestsView,
    ProposalCreateView,
    RequestProposalsView,
    AcceptProposalView,
    UpdateOrderStatusView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("", ServiceListView.as_view(), name="service-list"),
    path("request/create/", ServiceRequestCreateView.as_view(), name="create-request"),
    path("request/my/", MyServiceRequestsView.as_view(), name="my-requests"),
    path("proposal/create/", ProposalCreateView.as_view(), name="create-proposal"),
    path("proposal/accept/", AcceptProposalView.as_view(), name="accept-proposal"),
    path("message/send/", SendMessageView.as_view(), name="send-message"),
    path("report/create/", ReportCreateView.as_view(), name="create-report"),
    path("report/list/", ReportListView.as_view(), name="report-list"),
    path("review/create/", CreateReviewView.as_view(), name="create-review"),
    path(
        "order/status/update/",
        UpdateOrderStatusView.as_view(),
        name="update-order-status",
    ),
    path(
        "request/<int:request_id>/proposals/",
        RequestProposalsView.as_view(),
        name="request-proposals",
    ),
    path(
        "order/status/<int:request_id>/",
        OrderStatusDetailView.as_view(),
        name="order-status-detail",
    ),
    path(
        "request/<int:request_id>/scheduled-time/",
        ScheduledTimeView.as_view(),
        name="scheduled-time",
    ),
    path(
        "request/<int:request_id>/messages/",
        MessageListView.as_view(),
        name="message-list",
    ),
    path(
        "review/provider/<int:provider_id>/",
        ProviderReviewStatsView.as_view(),
        name="provider-reviews",
    ),
]
