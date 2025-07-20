from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, BatchViewSet, VesselViewSet, InventoryViewSet, SupplierViewSet, CustomerViewSet, PurchaseOrderViewSet, TimesheetViewSet, scan_inventory

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'batches', BatchViewSet)
router.register(r'vessels', VesselViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'timesheets', TimesheetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scan-inventory/', scan_inventory, name='scan-inventory'),
]