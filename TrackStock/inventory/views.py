from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    category_name = request.GET.get('category')
    if category_name:
        products = Product.objects.filter(category=category_name)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()  

    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories  
    })


