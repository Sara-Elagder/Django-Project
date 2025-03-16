from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Supermarket
from .forms import OrderForm, OrderItemFormSet, SupermarketForm
from inventory.models import Product, Category

@login_required
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

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
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def supermarket_list(request):
    supermarkets = Supermarket.objects.all()
    return render(request, 'orders/supermarket_list.html', {'supermarkets': supermarkets})

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
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, "Order deleted successfully.")
    return redirect(reverse('orders:order_list'))

@login_required
def delete_product(request, order_id, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order_id=order_id)

    if request.method == "POST":
        product = item.product

        # Remove the item from the order
        item.delete()

        messages.success(request, f"{product.name} was removed from the order, and stock was restored.")

    return redirect('orders:order_details', order_id=order_id)


@login_required
def add_product_to_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:  # Ensure both fields are filled
            messages.error(request, "Please select a product and enter a quantity.")
            return redirect("orders:order_details", order_id=order.id)

        try:
            quantity = int(quantity)  # Convert to integer
            if quantity <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return redirect("orders:order_details", order_id=order.id)
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect("orders:order_details", order_id=order.id)

        product = get_object_or_404(Product, id=product_id)

        # Ensure quantity is not greater than available stock
        if quantity > product.quantity:
            messages.error(request, f"Only {product.quantity} units available in stock.")
            return redirect("orders:order_details", order_id=order.id)

        # Call the method to add/update the product in the order
        order.add_product(product, quantity)

        messages.success(request, f"{quantity}x {product.name} added to the order.")
        return redirect("orders:order_details", order_id=order.id)

    return redirect("orders:order_details", order_id=order.id)  # Fallback redirect



@login_required
def edit_product_in_order(request, order_id, product_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        product = get_object_or_404(Product, id=product_id)
        new_quantity = request.POST.get("quantity")

        try:
            new_quantity = int(new_quantity)
            if new_quantity < 1:
                messages.error(request, "Quantity must be at least 1.")
                return redirect("orders:order_details", order_id=order.id)
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect("orders:order_details", order_id=order.id)

        order.update_product(product, new_quantity)
        messages.success(request, f"Quantity updated to {new_quantity} for {product.name}.")
        return redirect("orders:order_details", order_id=order.id)
