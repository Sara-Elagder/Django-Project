from django.contrib import admin
from .models import Order, Supermarket, OrderItem

admin.site.register(Order)
admin.site.register(Supermarket)
admin.site.register(OrderItem)

# Register your models here.

