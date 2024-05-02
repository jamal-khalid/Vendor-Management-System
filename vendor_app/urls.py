from django.urls import path 
from .views import VendorListCreateView , VendorRetriveUpdateDeleteView , PurchaseOrderListCreateView , PurchaseOrderRetriveUpdateDeleteView,VendorPerformanceView ,AcknowledgePurchaseOrderView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('vendors/' ,VendorListCreateView.as_view() ) , 
    path('vendors/<int:pk>/' , VendorRetriveUpdateDeleteView.as_view()),
    path('purchase_orders/' , PurchaseOrderListCreateView.as_view()),
    path('purchase_orders/<int:pk>/' , PurchaseOrderRetriveUpdateDeleteView.as_view()),
    path('vendors/<int:vendor_id>/performance/' , VendorPerformanceView.as_view()),
    path('purchase_orders/<int:pk>/acknowledge/' , AcknowledgePurchaseOrderView.as_view()),
    path('token/', obtain_auth_token, name='token_obtain_pair')
]

