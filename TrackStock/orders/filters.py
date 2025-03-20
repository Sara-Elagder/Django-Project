from django import forms
import django_filters
from .models import Order, Supermarket
from django.db.models.functions import TruncMonth, TruncYear, TruncDay

class OrderFilter(django_filters.FilterSet):
    supermarket_name = django_filters.ModelChoiceFilter(
        field_name='supermarket',
        queryset=Supermarket.objects.all(),
        label='Supermarket',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = django_filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_from = django_filters.DateFilter(
        field_name='date_created',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date From'
    )
    date_to = django_filters.DateFilter(
        field_name='date_created',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date To'
    )

    class Meta:
        model = Order
        fields = ['supermarket_name', 'status', 'date_from', 'date_to']