from django.apps import AppConfig


class MedicareappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medicareApp'

    def ready(self):
        import medicareApp.signals 