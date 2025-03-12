from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ProductForm, CategoryForm
from inventory.models import Product, Category

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if '_addanother' in request.POST:
                return redirect('shipment:add_product')
            else:
                return redirect('inventory:product_list')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Add Product',
    }
    return render(request, 'shipment/add_product.html', context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if '_addanother' in request.POST:
                return redirect('shipment:add_category')
            else:
                return redirect('inventory:product_list')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'title': 'Add Category',
    }
    return render(request, 'shipment/add_category.html', context)