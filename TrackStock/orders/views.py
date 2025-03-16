from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Supermarket
from .forms import OrderForm, OrderItemFormSet, SupermarketForm

@login_required
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.save()

            formset = OrderItemFormSet(request.POST, instance=order)

            if formset.is_valid():
                formset.save()
                return redirect('orders:order_list')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()

    context = {
        'order_form': order_form,
        'formset': formset,
    }
    return render(request, 'orders/create_order.html', context)

@login_required
def create_supermarket(request):
    if request.method == 'POST':
        form = SupermarketForm(request.POST)
        if form.is_valid():
            form.save()
            if '_addanother' in request.POST:
                return redirect('orders:create_supermarket')
            else:
                return redirect('orders:supermarket_list')
    else:
        form = SupermarketForm()

    context = {
        'form': form,
    }
    return render(request, 'orders/create_supermarket.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(created_by=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def supermarket_list(request):
    supermarkets = Supermarket.objects.all()
    return render(request, 'orders/supermarket_list.html', {'supermarkets': supermarkets})