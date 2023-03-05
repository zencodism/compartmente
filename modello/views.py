from django.shortcuts import render, redirect
from django.http import HttpResponse

from modello.models import *
from modello.modello import create_model

from collections import OrderedDict
from django.apps import apps
from django.conf import settings
from django.core import management
from importlib import import_module, reload
from django.urls import clear_url_caches

def make_sample_model():
    OtherProduct = create_model("OtherProduct", parent=Product, label="modello")
    OtherProduct._meta.app_config.verbose_name = "other"


import sys

def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        print(reload(sys.modules[settings.ROOT_URLCONF]))
        # reload(sys.modules[settings.ROOT_URLCONF])
    import_module(settings.ROOT_URLCONF)
    clear_url_caches()

def maker_view(request):

    # new_app_name = "newapp"
    #
    # settings.INSTALLED_APPS += (new_app_name, )
    # # To load the new app let's reset app_configs, the dictionary
    # # with the configuration of loaded apps
    # apps.app_configs = OrderedDict()
    # # set ready to false so that populate will work
    # apps.ready = False
    # # re-initialize them all; is there a way to add just one without reloading them all?
    # apps.populate(settings.INSTALLED_APPS)

    # print(DummyProduct.objects.count())
    #
    # DummySite = create_model("DummySite", parent=Site, label="modello")
    # print(DummySite.objects.count())
    #
    # SecondOne = create_model("SecondOne", parent=Product, label="modello")
    make_sample_model()
    reload_urlconf()
    return redirect('/admin')

# make_sample_model()
# reload_urlconf()
