from django.db import models
from django.conf import settings
from inventory.models import Product, Category
from django.core.exceptions import ValidationError

class Supermarket(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
    ]
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE ,default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    products = models.ManyToManyField(Product, through='OrderItem')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order for {self.supermarket.name} on {self.date_created.strftime('%Y-%m-%d')}"

    def add_product(self, product, quantity):

        if quantity > product.quantity:
            return "Not enough stock available."

        # Ensure quantity is always set
        order_item, created = OrderItem.objects.get_or_create(
            order=self,
            product=product,
            defaults={"quantity": 0}
        )

        if quantity > product.quantity:
            return f"Only {product.quantity} units available in stock."

        order_item.quantity += quantity
        product.quantity -= quantity
        product.save()
        order_item.save()
        return None

    def update_product(self, product, new_quantity):
        order_item = OrderItem.objects.filter(order=self, product=product).first()

        if order_item:
            stock_difference = new_quantity - order_item.quantity

            if stock_difference > product.quantity:
                return f"Not enough stock available for {product.name}."

            order_item.quantity = new_quantity
            product.quantity -= stock_difference

            product.save()
            order_item.save()
            return None
        return f"{product.name} is not in this order."

    def remove_product(self, product):
        order_item = OrderItem.objects.filter(order=self, product=product).first()

        if order_item:
            product.quantity += order_item.quantity
            product.save()
            order_item.delete()
        else:
            raise ValidationError(f"{product.name} is not in this order.")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"


    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

