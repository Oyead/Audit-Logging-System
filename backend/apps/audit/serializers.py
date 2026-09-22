from rest_framework import serializers
from apps.audit.models import AuditLogEntry
from apps.audit.services import append_entry

class AuditLogEntryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogEntry
        fields=["payload","actor_id"]
    def validate_payload(self,value):
        if not isinstance(value,dict) or not value:
            raise serializers.ValidationError("Payload must be a non-empty JSON object")
        if "action" not in value:
            raise serializers.ValidationError("Payload must contain an 'action' key.")
        return value
    def create(self,validated_data):
        payload = validated_data["payload"]
        actor_id = validated_data["actor_id"]
        return append_entry(payload=payload, actor_id=actor_id)

class AuditLogEntryReadSerializer(serializers.ModelSerializer):
    """
    Serializer used strictly for READING audit log entries.
    Exposes full cryptographic details to clients.
    """
    class Meta:
        model = AuditLogEntry
        fields = [
            "seq",
            "prev_hash",
            "hash",
            "payload",
            "actor_id",
            "created_at",
        ]
        read_only_fields = fields   