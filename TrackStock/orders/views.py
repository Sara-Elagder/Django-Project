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
from django.core.exceptions import ValidationError
from .filters import OrderFilter


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
                formset.save()
                messages.success(request, "Order created successfully.")
                return redirect('orders:order_list')
            else:
                order.delete()
                print(f"Formset errors: {formset.errors}")
                messages.error(request, "Please correct the errors in the order items.")
        else:
            formset = OrderItemFormSet(request.POST)
            print(f"Order form errors: {order_form.errors}")
            messages.error(request, "Please correct the errors in the order form.")
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

   if order.status == "Confirmed":
       messages.error(request, "You cannot delete the order as it has been already confirmed.")
       return redirect("orders:order_list")

   if request.method == "POST":

       for item in order.items.all():
           item.product.quantity += item.quantity
           item.product.save()

       order.delete()
       messages.success(request, "Order deleted successfully, and product stock has been restored.")

   return redirect(reverse('orders:order_list'))



@login_required
def delete_product(request, order_id, item_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "Confirmed" or order.status == "Loaded":
        messages.error(request, "You cannot add products to the order as it has been already loaded or confirmed.")
        return redirect("orders:order_details", order_id=order.id)

    item = get_object_or_404(OrderItem, id=item_id, order_id=order_id)


    if order.status == "Confirmed" or order.status == "Loaded":
        messages.error(request, "You cannot delete the order as it has been already loaded or confirmed.")
        return redirect("orders:order_details", order_id=order.id)


    if request.method == "POST":
        product = item.product

        item.delete()

        messages.success(request, f"{product.name} was removed from the order, and stock was restored.")

    return redirect('orders:order_details', order_id=order_id)


@login_required
def add_product_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "Confirmed" or order.status == "Loaded":
        messages.error(request, "You cannot add products to the order as it has been already loaded or confirmed.")
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

    if order.status == "Confirmed" or order.status == "Loaded":
        messages.error(request, "You cannot edit the order as it has been already loaded or confirmed.")
        return redirect("orders:order_details", order_id=order.id)

    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        new_quantity = request.POST.get("quantity")



        new_quantity = int(new_quantity)
        if new_quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect("orders:order_details", order_id=order.id)

        # Try updating the product without redirecting to an error page
        error_message = order.update_product(product, new_quantity)

        if error_message:  # If there's an error, show it to the user
            messages.error(request, error_message)
        else:
            messages.success(request, f"Quantity updated to {new_quantity} for {product.name}.")

    return redirect("orders:order_details", order_id=order.id)


@login_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Prevent further changes if the order is already confirmed
    if order.status == "Confirmed":
        messages.error(request, "You cannot change the status of a confirmed order.")
        return redirect("orders:order_details", order_id=order.id)

    if order.status == "Pending":
        order.status = "Loaded"
    elif order.status == "Loaded":
        order.status = "Confirmed"

    order.save()
    messages.success(request, f"Order status changed to {order.status}.")
    return redirect("orders:order_details", order_id=order.id)
