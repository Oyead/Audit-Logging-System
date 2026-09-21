from django.contrib import admin

from apps.audit.models import AuditEntry

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ("seq", "prev_hash", "hash", "payload", "created_at")
    list_display_links = ("seq",)