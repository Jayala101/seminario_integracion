# invoices/urls.py
from rest_framework.routers import DefaultRouter
from invoices.views.invoice import InvoiceViewSet
from invoices.views.detail import InvoiceDetailViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-details', InvoiceDetailViewSet, basename='invoice-detail')

urlpatterns = router.urls
