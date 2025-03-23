from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def product_list(request):
    category_id = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    products = Product.objects.all()

    # Apply search filter 
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

 
    if category_id:
        if category_id == 'low_stock':
 
            products = products.filter(quantity__gt=0, quantity__lte=5)
        elif category_id == 'zero_stock':
            products = products.filter(quantity=0)
        else:
            try:
                products = products.filter(category_id=category_id)
            except ValueError:
                pass
 
    category_selected = ''
    if category_id == 'low_stock':
        category_selected = 'Low Stock Items'
    elif category_id == 'zero_stock':
        category_selected = 'Out of Stock Items'
    elif category_id:
        try:
            category = Category.objects.get(id=category_id)
            category_selected = category.name
        except Category.DoesNotExist:
            pass
    elif search_query:
        category_selected = f'Search Results for: {search_query}'

    # Pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_selected': category_selected
    }
    return render(request, 'inventory/product_list.html', context)

