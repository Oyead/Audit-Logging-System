from django.conf import settings
from django.db import models


class AuditLogEntry(models.Model):
    seq = models.PositiveBigIntegerField(unique=True, db_index=True)
    prev_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    hash = models.CharField(max_length=64, unique=True)
    payload = models.JSONField()
    actor_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_index=True,
        related_name="audit_entries",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["seq"]

    def __str__(self):
        return f"AuditLogEntry(seq={self.seq})"


class ChainHead(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    last_seq = models.PositiveBigIntegerField()
    last_hash = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(id=1), name="chainhead_singleton")
        ]


class MerkleAnchor(models.Model):
    seq_start = models.PositiveBigIntegerField()
    seq_end = models.PositiveBigIntegerField()
    merkle_root = models.CharField(max_length=64)
    prev_root = models.CharField(max_length=64, null=True, blank=True)
    external_ref = models.CharField(max_length=255, blank=True)
    anchored_at = models.DateTimeField(auto_now_add=True)