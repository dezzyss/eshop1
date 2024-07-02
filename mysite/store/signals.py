from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Order)
def update_stock(sender, instance, **kwargs):
    if instance.complete:
        for item in instance.orderitem_set.all():
            product = item.product
            product.stock -= item.quantity
            product.save()