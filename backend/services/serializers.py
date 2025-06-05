from rest_framework import serializers
from .models import ServiceRequest, Proposal, Review, ChatMessage, SupportTicket


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"
        read_only_fields = ["customer", "created_at", "status"]


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = "__all__"
        read_only_fields = ["provider", "service_request", "created_at"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["customer", "provider", "service_request", "created_at"]


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = "__all__"
        read_only_fields = ["sender", "timestamp"]


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
