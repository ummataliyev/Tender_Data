from django.apps import AppConfig
from django.core.exceptions import ValidationError


class DataAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_app'

    def ready(self) -> None:
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        try:
            # Create an interval schedule for the first task
            schedule1, created1 = IntervalSchedule.objects.get_or_create(
                every=2,
                period=IntervalSchedule.MINUTES,
            )
            # Create the first periodic task
            PeriodicTask.objects.get_or_create(
                interval=schedule1,
                name='Abd Site Script',
                task='data_app.tasks.adb_script',
            )

            # Create an interval schedule for the second task
            schedule2, created2 = IntervalSchedule.objects.get_or_create(
                every=2,  # Change this to the desired interval in seconds
                period=IntervalSchedule.MINUTES,
            )
            # Create the second periodic task
            PeriodicTask.objects.get_or_create(
                interval=schedule2,
                name='Xt Site Scripts',
                task='data_app.tasks.xt_script',
            )

            # If you want to create a third task, repeat the process with a new schedule and task name.

        except ValidationError:
            pass

        return super().ready()
