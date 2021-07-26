from django.apps import AppConfig


class datumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'datum'

    def ready(self):
        from datum import signals