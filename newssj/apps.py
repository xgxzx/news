from django.apps import AppConfig


class NewssjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newssj'

    def ready(self):
        from newssj import signals
        # выполнение модуля -> регистрация сигналов
