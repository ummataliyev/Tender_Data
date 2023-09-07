from django.db import models
from django.utils import timezone


class Job(models.Model):
    company_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    deadline = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.company_name} - Tender is active: {self.is_active}, Deadline to: {self.deadline}"
