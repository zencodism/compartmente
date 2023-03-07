import json
import sys
from importlib import import_module, reload

from django.conf import settings
from django.contrib import admin
from django.urls import clear_url_caches

from .models import Tenant, Product, Site, Staff
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
        NewSite = create_model(f"{obj.name}_Site", parent=Site, label="modello")
        NewStaff = create_model(f"{obj.name}_Staff", parent=Staff, label="modello", target=NewSite)
        the_label = obj.name.lower()
        NewProduct._meta.app_config.verbose_name = the_label

        try:
            admin.site.register(NewProduct)
            admin.site.register(NewSite)
            admin.site.register(NewStaff)
        except admin.sites.AlreadyRegistered:
            pass

        Tenant.objects.update(active=False)

        apps = admin.site.get_app_list(request, app_label="modello")
        for model in apps[0]["models"]:
            if model["object_name"] == "Tenant":
                continue
            if obj.name in model["name"] and obj.active:
                continue
            else:
                try:
                    admin.site.unregister(model["model"])
                except admin.sites.NotRegistered:
                    pass

        reload_urlconf()
        return super(TenantAdmin, self).save_model(request, obj, form, change)

admin.site.register(Tenant, TenantAdmin)
