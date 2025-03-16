from django.db import models
from inventory.models import Product  

class Shipment(models.Model):
    factory_name = models.CharField(max_length=255, default="Default Factory")
    date_received = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Received', 'Received')],
        default='Pending'
    )
    products = models.ManyToManyField(Product, through='ShipmentItem')

    def __str__(self):
        return f"Shipment from {self.factory_name} on {self.date_received}"

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.shipment}"
