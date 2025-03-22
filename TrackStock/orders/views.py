from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order, OrderItem, Supermarket
from .forms import OrderForm, OrderItemFormSet, SupermarketForm
from inventory.models import Product, Category
from .decorators import manager_required
from django.core.exceptions import ValidationError
from .filters import OrderFilter
from collections import defaultdict

@login_required
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.status = 'Pending'
            order.save()

            formset = OrderItemFormSet(request.POST, instance=order)

            if formset.is_valid():
                insufficient_stock = []
                product_quantities = defaultdict(int)

                for form in formset:
                    if form.cleaned_data:
                        product = form.cleaned_data["product"]
                        quantity = form.cleaned_data["quantity"]
                        product_quantities[product] += quantity

                for product, total_quantity in product_quantities.items():
                    if total_quantity > product.quantity:
                        insufficient_stock.append(f"{product.name} (Available: {product.quantity})")

                if insufficient_stock:
                    order.delete()
                    messages.error(request, f"Not enough stock for: {', '.join(insufficient_stock)}.")
                else:

                    for product, total_quantity in product_quantities.items():
                        product.quantity -= total_quantity
                        product.save()


                        order_item, created = OrderItem.objects.get_or_create(
                            order=order,
                            product=product,
                            defaults={'quantity': 0}
                        )
                        order_item.quantity += total_quantity
                        order_item.save()

                    messages.success(request, "Order created successfully.")
                    return redirect('orders:order_list')

            else:
                order.delete()
                messages.error(request, "Please correct the errors in the order items.")

        else:
            messages.error(request, "Please correct the errors in the order form.")

    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/create_order.html', {'order_form': order_form, 'formset': formset})


@login_required
@manager_required
def create_supermarket(request):
    if request.method == 'POST':
        form = SupermarketForm(request.POST)
        if form.is_valid():
            form.save()
            if '_addanother' in request.POST:
                return redirect('orders:create_supermarket')
            else:
                return redirect('orders:create_order')
    else:
        form = SupermarketForm()

    context = {
        'form': form,
    }
    return render(request, 'orders/create_supermarket.html', context)

@login_required
def order_list(request):
    orders = Order.objects.all()
    order_filter = OrderFilter(request.GET, queryset=orders)

    context = {
        'filter': order_filter,
        'orders': order_filter.qs
    }
    return render(request, 'orders/order_list.html', context)

@login_required
def supermarket_list(request):
    supermarkets = Supermarket.objects.annotate(order_count=Count("order"))
    return render(request, "orders/supermarket_list.html", {"supermarkets": supermarkets})


@login_required
@manager_required
def delete_supermarket(request, supermarket_id):
    supermarket = get_object_or_404(Supermarket, id=supermarket_id)

    with transaction.atomic():

        orders = Order.objects.filter(supermarket=supermarket)

        for order in orders:
            if order.status in ["Pending", "Loaded"]:

                for item in order.items.all():
                    item.product.quantity += item.quantity
                    item.product.save()

        orders.delete()

        supermarket.delete()

        messages.success(request, "Supermarket and related orders have been deleted.")

    return redirect("orders:supermarket_list")



@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    products = Product.objects.all()
    categories = set(product.category for product in products)
    return render(request, 'orders/order_details.html', {
        'order': order,
        'products': products,
        'categories': categories
    })

@login_required
def order_delete(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status == "Confirmed" or order.status == "Delivered":
        messages.error(request, "You cannot delete the order as it has been already confirmed or delivered.")
        return redirect("orders:order_details", order_id=order.id)

    if request.method == "POST":

        for item in order.items.all():
            item.product.quantity += item.quantity
            item.product.save()

        order.delete()
        messages.success(request, "Order deleted successfully, and product stock has been restored.")

    return redirect(reverse('orders:order_list'))
#


@login_required
def delete_product(request, order_id, item_id):
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order_id=order_id)

    if order.status == "Confirmed" or order.status == "Delivered":
        messages.error(request, "You cannot delete the product as it has been already confirmed or delivered.")
        return redirect("orders:order_details", order_id=order.id)

    if request.method == "POST":
        product = item.product

        item.delete()

        messages.success(request, f"{product.name} was removed from the order, and stock was restored.")

    return redirect('orders:order_details', order_id=order_id)


@login_required
def add_product_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "Confirmed" or order.status == "Delivered":
        messages.error(request, "You cannot add the product as it has been already confirmed or delivered.")
        return redirect("orders:order_details", order_id=order.id)

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")


        if not product_id or not quantity:
            messages.error(request, "Please select a product and enter a quantity.")
            return redirect("orders:order_details", order_id=order.id)

        quantity = int(quantity)
        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect("orders:order_details", order_id=order.id)

        product = get_object_or_404(Product, id=product_id)

        error_message = order.add_product(product, quantity)

        if error_message:
            messages.error(request, error_message)
        else:
            messages.success(request, f"{quantity}x {product.name} added to the order.")

    return redirect("orders:order_details", order_id=order.id)



@login_required
def edit_product_in_order(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "Confirmed" or order.status == "Delivered":
        messages.error(request, "You cannot edit the order as it has been already confirmed or delivered.")
        return redirect("orders:order_details", order_id=order.id)

    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        new_quantity = request.POST.get("quantity")



        new_quantity = int(new_quantity)
        if new_quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect("orders:order_details", order_id=order.id)

        error_message = order.update_product(product, new_quantity)

        if error_message:  # If there's an error, show it to the user
            messages.error(request, error_message)
        else:
            messages.success(request, f"Quantity updated to {new_quantity} for {product.name}.")

    return redirect("orders:order_details", order_id=order.id)


@login_required
@manager_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "Delivered":
        messages.error(request, "You cannot change the status of a delivered order.")
        return redirect("orders:order_details", order_id=order.id)

    if order.status == "Pending":
        order.status = "Confirmed"
    elif order.status == "Confirmed":
        order.status = "Delivered"

    order.save()
    messages.success(request, f"Order status changed to {order.status}.")
    return redirect("orders:order_details", order_id=order.id)
