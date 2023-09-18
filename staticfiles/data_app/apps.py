import logging

from django.apps import AppConfig
from django.db.utils import ProgrammingError
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


class DataAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_app'

    def ready(self) -> None:
        from django_celery_beat.models import PeriodicTask
        from django_celery_beat.models import IntervalSchedule
        try:
            # Create an interval schedule for the first task
            schedule1, created1 = IntervalSchedule.objects.get_or_create(
                every=8,
                period=IntervalSchedule.HOURS,
            )
            if created1:
                # Create the first periodic task
                PeriodicTask.objects.get_or_create(
                    interval=schedule1,
                    name='Abd Site Script',
                    task='data_app.tasks.adb_script',
                )
        except (ProgrammingError, ValidationError) as exc:
            logger.error("Ignoring validation and programming error for celery task - %s", exc)

        return super().ready()
