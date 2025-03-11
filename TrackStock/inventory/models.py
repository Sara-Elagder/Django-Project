from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True)
    critical_level = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)

    def is_critical(self):
        return self.quantity < self.critical_level

    def __str__(self):
        return self.name