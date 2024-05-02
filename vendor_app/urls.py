from django.urls import path 
from .views import VendorListCreateView , VendorRetriveUpdateDeleteView , PurchaseOrderListCreateView , PurchaseOrderRetriveUpdateDeleteView,VendorPerformanceView ,AcknowledgePurchaseOrderView

urlpatterns = [
    path('vendors/' ,VendorListCreateView.as_view() ) , 
    path('vendors/<int:pk>' , VendorRetriveUpdateDeleteView.as_view()),
    path('purchase_orders/' , PurchaseOrderListCreateView.as_view()),
    path('purchase_orders/<int:pk>/' , PurchaseOrderRetriveUpdateDeleteView.as_view()),
    path('vendors/<int:vendor_id>/performance/' , VendorPerformanceView.as_view()),
    path('purchase_orders/<int:pk>/acknowledge/' , AcknowledgePurchaseOrderView.as_view())
]

