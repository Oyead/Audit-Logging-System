from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from apps.audit.models import AuditLogEntry
from apps.audit.serializers import (
    AuditLogEntryReadSerializer,
    AuditLogEntryWriteSerializer,
)


class StandardAuditLogPagination(PageNumberPagination):
    """
    Paginates audit log results to prevent loading excessive records at once.
    """
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class AuditLogEntryListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/audit/entries/ — Browse audit log history.
    POST /api/audit/entries/ — Append new audit log.
    """
    queryset = AuditLogEntry.objects.all().order_by("seq")
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardAuditLogPagination

    def get_serializer_class(self):
        """
        Use the write serializer for POST requests to validate and append logs,
        and the read serializer for GET requests to output full cryptographic fields.
        """
        if self.request.method == "POST":
            return AuditLogEntryWriteSerializer
        return AuditLogEntryReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests. After the write serializer creates the entry,
        returns the newly created entry formatted using the read serializer.
        """
        response = super().create(request, *args, **kwargs)
        
        # Re-serialize the created object using the Read Serializer
        # so the API client receives the generated seq, prev_hash, and hash.
        instance = AuditLogEntry.objects.get(seq=response.data["seq"])
        read_serializer = AuditLogEntryReadSerializer(instance)
        
        response.data = read_serializer.data
        return response