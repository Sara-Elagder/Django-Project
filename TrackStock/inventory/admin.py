from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'is_critical', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'image')
        }),
        ('Inventory Details', {
            'fields': ('quantity', 'critical_level')
        }),
    )

admin.site.register(Product, ProductAdmin)