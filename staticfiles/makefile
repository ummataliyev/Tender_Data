run-rabbit-mq:
	docker run --detach --name rabbitmq --publish 5672:5672 --publish 15672:15672 --restart unless-stopped rabbitmq:management

celery-info:
	celery -A tender_config worker -l INFO

celery-beat-info:
	celery -A tender_config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
