<<<<<<< HEAD
from django.apps import AppConfig


=======
# invoices/apps.py
from django.apps import AppConfig

>>>>>>> ab7a16d92c366da0755c358a0b4f9e64d59831d1
class InvoicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoices'

    def ready(self):
<<<<<<< HEAD
        import invoices.signals  # noqa
=======
        import invoices.signals  # noqa
>>>>>>> ab7a16d92c366da0755c358a0b4f9e64d59831d1
