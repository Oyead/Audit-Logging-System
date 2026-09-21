from django.db import transaction

from apps.audit.hashing import compute_entry_hash
from apps.audit.models import AuditLogEntry, ChainHead


def append_entry(payload: dict, actor_id=None) -> AuditLogEntry:
    with transaction.atomic():
        head, _ = ChainHead.objects.select_for_update().get_or_create(
            pk=1, defaults={"last_seq": 0, "last_hash": ""}
        )
        seq = head.last_seq + 1
        prev_hash = head.last_hash or None
        entry = AuditLogEntry.objects.create(
            seq=seq,
            prev_hash=prev_hash,
            hash=compute_entry_hash(seq, prev_hash, payload),
            payload=payload,
            actor_id=actor_id,
        )
        head.last_seq = seq
        head.last_hash = entry.hash
        head.save(update_fields=["last_seq", "last_hash"])
    return entry