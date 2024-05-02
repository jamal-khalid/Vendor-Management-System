from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from django.db.models import Avg, Count
from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, created, **kwargs):
    vendor = instance.vendor

    # Calculate On-Time Delivery Rate
    if instance.status == 'completed':
        total_completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=instance.delivery_date).count()
        vendor.on_time_delivery_rate = (on_time_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0

    # Calculate Quality Rating Average
    if instance.quality_rating is not None:
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
        vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg else 0


    # Calculate Fulfilment Rate
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    vendor.fulfillment_rate = (fulfilled_pos / total_pos) * 100 if total_pos > 0 else 0

    # Save vendor instance
    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    vendor = instance.vendor
    
    response_times = PurchaseOrder.objects.filter(vendor=vendor).exclude(acknowledgment_date=None).values_list('acknowledgment_date', 'order_date')
    if response_times:
        average_response_time = sum((ack_date - order_date).total_seconds() for ack_date, order_date in response_times) / len(response_times)
    else:
        average_response_time = 0  # Default to 0 if no relevant orders exist

    vendor.average_response_time = average_response_time
    vendor.save()

@receiver(post_save, sender=Vendor)
def update_historical_performance(sender, instance, created, **kwargs):
    if not created:  # Only update historical performance on updates, not creation
        HistoricalPerformance.objects.create(
            vendor=instance,
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            average_response_time=instance.average_response_time,
            fulfillment_rate=instance.fulfillment_rate
        )