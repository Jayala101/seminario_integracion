from django.apps import AppConfig


class InvoicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoices'
    verbose_name = 'Reservas de Vuelos'
    
    def ready(self):
        import invoices.signals
