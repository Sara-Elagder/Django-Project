from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Shipment, ShipmentItem
from inventory.models import Product, Category

class ProductInShipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'is_critical')
    list_filter = ('category', 'is_critical')
    search_fields = ('name',)

    autocomplete_fields = ('category',)

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('admin:inventory_product_add'))
        else:
            return HttpResponseRedirect(reverse('admin:inventory_product_changelist'))

    def response_change(self, request, obj):
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('admin:inventory_product_add'))
        else:
            return HttpResponseRedirect(reverse('admin:inventory_product_changelist'))

class CategoryInShipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('admin:inventory_category_add'))
        else:
            return HttpResponseRedirect(reverse('admin:inventory_category_changelist'))

    def response_change(self, request, obj):
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('admin:inventory_category_add'))
        else:
            return HttpResponseRedirect(reverse('admin:inventory_category_changelist'))

class ShipmentItemInline(admin.TabularInline):
    model = ShipmentItem
    extra = 1
    autocomplete_fields = ('product',)

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'shipment_date')
    search_fields = ('reference_number',)
    inlines = [ShipmentItemInline]


admin.site.register(Shipment, ShipmentAdmin)

