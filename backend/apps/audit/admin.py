from django.contrib import admin

from apps.audit.models import AuditLogEntry

@admin.register(AuditLogEntry)
class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ("seq", "prev_hash", "hash", "actor_id", "payload", "created_at")
    list_display_links = ("seq",)