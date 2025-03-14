from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'get_stock_status', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'image')
        }),
        ('Inventory Details', {
            'fields': ('quantity', 'critical_level')
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)  
