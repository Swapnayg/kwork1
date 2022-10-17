from django.apps import AppConfig


class EducaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kworkapp'
    verbose_name = 'Letworkbedone'
    def ready(self):
        from . import updater
        updater.start()
