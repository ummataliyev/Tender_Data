from django.db import models


class Job(models.Model):
    company_name = models.CharField(max_length=255)
    link = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.company_name} - Tender link: {self.link}, Status: {self.is_active}"
