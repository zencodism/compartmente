from django.apps import AppConfig

# from .models import Product, Site

class ModelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modello'

    def ready(self):
        print("Wat.")
