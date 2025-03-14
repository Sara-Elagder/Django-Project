from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/category/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  
    critical_level = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)

    def get_stock_status(self):
        if self.quantity == 0:
            return "out_of_stock"
        elif self.quantity < self.critical_level:
            return "low_stock"
        else:
            return "in_stock"


    def __str__(self):
        return self.name
