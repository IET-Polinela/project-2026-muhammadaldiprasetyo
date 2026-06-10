from django.db import models
from django.conf import settings
from django.db.models import Q


class ReportQuerySet(models.QuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()

        if user.is_admin:
            return self.filter(
                status__in=[
                    Report.Status.REPORTED,
                    Report.Status.VERIFIED,
                    Report.Status.IN_PROGRESS,
                    Report.Status.RESOLVED,
                ]
            )

        return self.filter(
            Q(reporter=user, status=Report.Status.DRAFT)
            | ~Q(status=Report.Status.DRAFT)
        )

class Report(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        REPORTED = 'REPORTED', 'Reported'
        VERIFIED = 'VERIFIED', 'Verified'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReportQuerySet.as_manager()

    def __str__(self):
        return self.title

    def can_edit(self, user):
        return (
            user.is_authenticated
            and not user.is_admin
            and self.reporter_id == user.id
            and self.status == self.Status.DRAFT
        )

    def can_delete(self, user):
        return self.can_edit(user)

    def can_submit(self, user):
        return self.can_edit(user)

    def can_verify(self, user):
        return self.can_update_status(user)

    def can_update_status(self, user):
        return (
            user.is_authenticated
            and user.is_admin
            and self.next_workflow_status() is not None
        )

    def next_workflow_status(self):
        transitions = {
            self.Status.REPORTED: self.Status.VERIFIED,
            self.Status.VERIFIED: self.Status.IN_PROGRESS,
            self.Status.IN_PROGRESS: self.Status.RESOLVED,
        }
        return transitions.get(self.status)

    def next_workflow_label(self):
        next_status = self.next_workflow_status()
        if next_status is None:
            return ""
        return self.Status(next_status).label

    def next_workflow_action_label(self):
        actions = {
            self.Status.REPORTED: "Verifikasi",
            self.Status.VERIFIED: "Proses",
            self.Status.IN_PROGRESS: "Selesaikan",
        }
        return actions.get(self.status, "")
