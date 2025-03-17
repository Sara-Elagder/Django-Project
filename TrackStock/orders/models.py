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
        ('Loaded', 'Loaded'),
        ('Confirmed', 'Confirmed'),
    ]
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE ,default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    products = models.ManyToManyField(Product, through='OrderItem')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order for {self.supermarket.name} on {self.date_created.strftime('%Y-%m-%d')}"

    def add_product(self, product, quantity):
        """Adds a product to the order, updates quantity if it exists, and adjusts stock"""
        if quantity > product.quantity:
            raise ValidationError(f"Not enough stock available for {product.name}.")

        # Get or create the order item
        order_item, created = OrderItem.objects.get_or_create(
            order=self, product=product, defaults={"quantity": 0}  # Ensure quantity is set
        )

        if not created:
            # Ensure we don't exceed available stock
            if order_item.quantity + quantity > product.quantity:
                raise ValidationError(f"Not enough stock available for {product.name}.")
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity  # Set quantity if newly created

        # Adjust product stock
        product.quantity -= quantity
        product.save()

        order_item.save()

    def update_product(self, product, new_quantity):
        """Updates the quantity of a product in the order and adjusts stock"""
        order_item = OrderItem.objects.filter(order=self, product=product).first()

        if order_item:
            stock_difference = new_quantity - order_item.quantity

            if stock_difference > product.quantity:
                raise ValidationError(f"Not enough stock available for {product.name}.")

            order_item.quantity = new_quantity
            product.quantity -= stock_difference  # Adjust stock

            product.save()
            order_item.save()
        else:
            raise ValidationError(f"{product.name} is not in this order.")

    def remove_product(self, product):
        """Removes a product from the order and restores stock"""
        order_item = OrderItem.objects.filter(order=self, product=product).first()

        if order_item:
            product.quantity += order_item.quantity  # Restore stock
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
        """Restore stock when an order item is deleted"""
        self.product.quantity += self.quantity  # Restore stock
        self.product.save()
        super().delete(*args, **kwargs)
