from django.urls import path
from apps.audit.views import AuditLogEntryListCreateView

urlpatterns = [
    path("entries/", AuditLogEntryListCreateView.as_view(), name="audit-log-entries"),
]