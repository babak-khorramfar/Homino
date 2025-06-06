from django.urls import path
from services.api_views import (
    CategoryListView,
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
]
