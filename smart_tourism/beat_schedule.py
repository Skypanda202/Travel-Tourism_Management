from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {

    'aggregate-daily-analytics': {

        'task': 'apps.analytics.tasks.aggregate_daily_analytics',

        'schedule': crontab(hour=0, minute=5),
    },

    'aggregate-place-analytics': {

        'task': 'apps.analytics.tasks.aggregate_place_analytics',

        'schedule': crontab(hour=0, minute=15),
    },
}