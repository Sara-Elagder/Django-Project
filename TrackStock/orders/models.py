from django.db import models
from django.conf import settings
from inventory.models import Product

class Supermarket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    ]
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE ,default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    products = models.ManyToManyField(Product, through='OrderItem')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order for {self.supermarket.name} on {self.date_created.strftime('%Y-%m-%d')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"