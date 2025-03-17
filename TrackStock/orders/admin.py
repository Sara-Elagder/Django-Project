from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem, Supermarket

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'supermarket', 'date_created', 'status', 'created_by', 'view_order_link']
    list_filter = ['status', 'supermarket']
    search_fields = ['supermarket__name', 'created_by__username']
    date_hierarchy = 'date_created'
    inlines = [OrderItemInline]

    def view_order_link(self, obj):
        url = reverse('orders:order_details', args=[obj.id])
        return format_html('<a href="{}" class="button">View Order</a>', url)

    view_order_link.short_description = 'View Order'

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on new instances
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Supermarket)
class SupermarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name', 'location']
