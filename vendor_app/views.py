from django.shortcuts import render
from .models import Vendor , HistoricalPerformance , PurchaseOrder
from . serializers import VendorSerializer , PurchaseOrderSerializer , VendorPerformanceSerializer
from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime 
from .signals import update_average_response_time
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer 


class VendorRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer 


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer 


class PurchaseOrderRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer 

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_url_kwarg = 'vendor_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.acknowledgment_date = datetime.now()
            instance.save()
            # Trigger recalculation of average_response_time
            update_average_response_time(sender=PurchaseOrder, instance=instance, created=False)
            return Response("Purchase order acknowledged successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


