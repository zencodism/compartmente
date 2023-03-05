import sys
from importlib import import_module, reload

from django.conf import settings
from django.contrib import admin
from django.urls import clear_url_caches

from .models import Tenant, Product, Site
from .modello import create_model


def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    import_module(settings.ROOT_URLCONF)
    clear_url_caches()

class TenantAdmin(admin.ModelAdmin):
    list_display =  ("id", "name", "active", )
    list_editable = ("name", "active", )
    def save_model(self, request, obj, form, change):
        NewProduct = create_model(f"{obj.name}_Product", parent=Product, label="modello")
        NewSite = create_model(f"{obj.name}_Site", parent=Product, label="modello")
        NewProduct._meta.app_config.verbose_name = obj.name.lower()
        reload_urlconf()
        return super(TenantAdmin, self).save_model(request, obj, form, change)

admin.site.register(Tenant, TenantAdmin)
