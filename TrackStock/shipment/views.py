from .forms import ProductForm, CategoryForm,ShipmentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Shipment, ShipmentItem
from inventory.models import Category , Product
from django.utils.timezone import now
from django.urls import reverse
from django.contrib import messages
from .forms import ShipmentItemForm

def shipment_list(request):
    shipments = Shipment.objects.all()
    return render(request, 'shipment/shipment_list.html', {'shipments': shipments})

def shipment_create(request):
    if request.method == "POST":
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save()
            return redirect(reverse('shipment:shipment_detail', args=[shipment.id]))
    else:
        form = ShipmentForm()
    return render(request, 'shipment/shipment_form.html', {'form': form})


def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment_items = ShipmentItem.objects.filter(shipment=shipment)  

    return render(request, 'shipment/shipment_detail.html', {
        'shipment': shipment,
        'shipment_items': shipment_items,  
    })



def add_product_to_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    products = Product.objects.all()  
    categories = set(product.category for product in products)  

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")

        try:
            product = Product.objects.get(id=product_id)
            quantity = int(quantity)

            shipment_item, created = ShipmentItem.objects.get_or_create(
                shipment=shipment,
                product=product,
                defaults={"quantity": quantity}
            )

            if not created:
                shipment_item.quantity += quantity
                shipment_item.save()

            return redirect('shipment:shipment_detail', shipment_id=shipment.id)

        except (Product.DoesNotExist, ValueError):
            pass  

    return render(request, "shipment/add_product_to_shipment.html", {
        "shipment": shipment,
        "products": products,
        "categories": categories
    })

def finish_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    if shipment.status == "Pending":
        shipment.status = "Loaded"
        shipment.save()
    return redirect(reverse('shipment:shipment_detail', args=[shipment.id]))

def update_shipment_status(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    if shipment.status == "Loaded":  
        shipment.status = "Received"
        shipment.date_received = now()  
        shipment.save()
    return redirect(reverse('shipment:shipment_detail', args=[shipment.id]))

def shipment_delete(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.delete()
    return redirect(reverse('shipment:shipment_list'))

def edit_product(request, shipment_id, item_id):
    item = get_object_or_404(ShipmentItem, id=item_id, shipment_id=shipment_id)

    if request.method == 'POST':
        form = ShipmentItemForm(request.POST, instance=item)  
        print("POST Data:", request.POST)  
        if form.is_valid():
            form.save()
            return redirect('shipment:shipment_detail', shipment_id=shipment_id)
        else:
            print("Form is not valid:", form.errors)  

    else:
        form = ShipmentItemForm(instance=item)

    return render(request, 'shipment/edit_product.html', {'form': form, 'shipment': item.shipment, 'product': item.product})



def delete_product(request, shipment_id, item_id):
    item = get_object_or_404(ShipmentItem, id=item_id, shipment_id=shipment_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Product deleted successfully.")
    return redirect('shipment:shipment_detail', shipment_id=shipment_id)

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