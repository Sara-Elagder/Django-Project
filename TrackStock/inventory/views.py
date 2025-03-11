from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Product
from .forms import ProductForm

class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('product_added')

def product_added(request):
    return render(request, 'inventory/product_added.html')