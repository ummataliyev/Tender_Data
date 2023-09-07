from django.db import models
from django.utils import timezone


class Job(models.Model):
    company_name = models.CharField(max_length=255)
    deadline = models.BooleanField(default=True)
    published = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.company_name
