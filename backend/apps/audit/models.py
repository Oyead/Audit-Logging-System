from django.db import models


class AuditEntry(models.Model):
    seq = models.PositiveBigIntegerField(unique=True, db_index=True)
    prev_hash = models.CharField(max_length=64, default="0" * 64)
    hash = models.CharField(max_length=64, unique=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["seq"]

    def __str__(self):
        return f"AuditEntry(seq={self.seq})"