from django import forms
from inventory.models import Product, Category
from .models import Shipment, ShipmentItem
from django.core.exceptions import ValidationError
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'category', 'critical_level', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'critical_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
        
def validate_factory_name(value):
    if not re.match(r'^[A-Za-z\s]+$', value):
        raise ValidationError("Factory name must contain only letters and spaces.")

class ShipmentForm(forms.ModelForm):
    factory_name = forms.CharField(validators=[validate_factory_name])

    class Meta:
        model = Shipment
        fields = ['factory_name']



class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ['product', 'quantity']
        widgets = {
             'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 2147483647}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['readonly'] = True  
