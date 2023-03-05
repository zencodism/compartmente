from django.apps import AppConfig

# from .views import make_sample_model, reload_urlconf

class ModelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modello'

    def ready(self):
        # make_sample_model()
        # reload_urlconf()
        pass
