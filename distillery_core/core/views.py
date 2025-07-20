from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe, Batch, Vessel, Inventory, Supplier, Customer, PurchaseOrder, Timesheet
from .serializers import RecipeSerializer, BatchSerializer, VesselSerializer, InventorySerializer, SupplierSerializer, CustomerSerializer, PurchaseOrderSerializer, TimesheetSerializer, ScanInventorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

class VesselViewSet(viewsets.ModelViewSet):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer

@api_view(['POST'])
def scan_inventory(request):
    serializer = ScanInventorySerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        action = serializer.validated_data['action']
        quantity = serializer.validated_data['quantity']
        try:
            item = Inventory.objects.get(barcode=code)
            if action == 'add':
                item.quantity += quantity
            elif action == 'remove':
                item.quantity -= quantity
            item.save()
            return Response(InventorySerializer(item).data)
        except Inventory.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)
    return Response(serializer.errors, status=400)