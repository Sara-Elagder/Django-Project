from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    category_name = request.GET.get('category')
    category_selected = "All Products"

    if category_name == "low_stock":
        products = Product.objects.all()
        products = [product for product in products if product.is_critical()]
        category_selected = "Low Stock"
    elif category_name == "zero_stock":
        products = Product.objects.filter(quantity=0)
        category_selected = "Out of Stock"
    elif category_name:
        category_selected = get_object_or_404(Category, id=category_name)
        products = Product.objects.filter(category=category_name)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'inventory/product_list.html', {
        'products': page_obj,
        'categories': categories,
        'category_selected': category_selected
    })

