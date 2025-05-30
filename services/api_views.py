from rest_framework import generics, permissions
from .models import ServiceRequest, Proposal, Review, ChatMessage, SupportTicket
from .serializers import (
    ServiceRequestSerializer,
    ProposalSerializer,
    ReviewSerializer,
    ChatMessageSerializer,
    SupportTicketSerializer,
)


class ServiceRequestCreateAPI(generics.CreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class ProposalCreateAPI(generics.CreateAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            provider=self.request.user, service_request_id=self.kwargs["request_id"]
        )


class ReviewCreateAPI(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        request_obj = ServiceRequest.objects.get(pk=self.kwargs["request_id"])
        provider = request_obj.proposals.filter(is_accepted=True).first().provider
        serializer.save(
            customer=self.request.user, service_request=request_obj, provider=provider
        )


class ChatMessageCreateAPI(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user, receiver_id=self.kwargs["receiver_id"]
        )


class SupportTicketCreateAPI(generics.CreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
