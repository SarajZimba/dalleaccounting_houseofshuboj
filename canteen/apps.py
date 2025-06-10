from django.apps import AppConfig

class CanteenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'canteen'

    # def ready(self):
    #     from canteen.scheduler import schedule_job
    #     schedule_job()
