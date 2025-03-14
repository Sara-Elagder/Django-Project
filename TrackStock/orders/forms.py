from django import forms
from .models import Order, OrderItem, Supermarket
from inventory.models import Product

class SupermarketForm(forms.ModelForm):
    class Meta:
        model = Supermarket
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supermarket', 'status']
        widgets = {
            'supermarket': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)