from django.apps import AppConfig


class NewsPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsPortal'

    def ready(self):
        import NewsPortal.signals
