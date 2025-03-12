from django.db import models
from inventory.models import Product, Category

class Shipment(models.Model):
    reference_number = models.CharField(max_length=100, unique=True)
    shipment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Shipment #{self.reference_number}"

    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = "Shipment Item"
        verbose_name_plural = "Shipment Items"