from django.apps import AppConfig
from .services.text_to_speech import tts


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        tts.init_model()
