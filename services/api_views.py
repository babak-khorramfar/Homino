from rest_framework import generics, permissions
from .models import ServiceRequest, Proposal, Review, ChatMessage, SupportTicket
from .serializers import (
    ServiceRequestSerializer,
    ProposalSerializer,
    ReviewSerializer,
    ChatMessageSerializer,
    SupportTicketSerializer,
)


class ServiceRequestCreateAPI(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProposalCreateAPI(generics.CreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReviewCreateAPI(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatMessageCreateAPI(generics.CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupportTicketCreateAPI(generics.CreateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
