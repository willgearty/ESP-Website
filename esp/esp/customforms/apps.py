from django.db.models import signals
from django.apps import AppConfig

def run_install(sender, **kwargs):
    if sender.name == 'esp.customforms':
        sender.models_module.install()

class CustomformsConfig(AppConfig):
    name = 'esp.customforms'

    def ready(self):
        signals.post_migrate.connect(run_install)