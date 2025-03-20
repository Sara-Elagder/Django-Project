import django_filters
from django import forms
from .models import Shipment
import datetime

class ShipmentFilter(django_filters.FilterSet):
    def factory_name_choices():
        factory_names = Shipment.objects.values_list('factory_name', flat=True).distinct().order_by('factory_name')
        return [(name, name) for name in factory_names]

    factory_name = django_filters.ChoiceFilter(
        choices=factory_name_choices,
        empty_label="All Factories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = django_filters.ChoiceFilter(
        choices=Shipment._meta.get_field('status').choices,
        empty_label="All Statuses",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_received_min = django_filters.DateFilter(
        field_name='date_received',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='From Date'
    )

    date_received_max = django_filters.DateFilter(
        field_name='date_received',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='To Date'
    )

    class Meta:
        model = Shipment
        fields = ['factory_name', 'status', 'date_received_min', 'date_received_max']