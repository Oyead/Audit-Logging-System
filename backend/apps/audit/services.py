from apps.audit.hashing import compute_entry_hash
from apps.audit.models import AuditEntry
def append_entry(payload: dict) -> AuditEntry:
    last =AuditEntry.objects.order_by("seq").last()
    seq =last.seq + 1 if last else 1
    prev_hash = last.hash if last else "0" * 64
    return AuditEntry.objects.create(
        seq=seq,
        prev_hash=prev_hash,
        hash=compute_entry_hash(seq, prev_hash, payload),
        payload=payload,
    )