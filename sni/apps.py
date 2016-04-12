from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "sni"

    def ready(self):
        import_module("sni.receivers")
