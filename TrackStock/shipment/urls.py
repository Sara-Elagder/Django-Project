from django.urls import path
from . import views
from .views import (
    shipment_list, shipment_create, shipment_detail,
    add_product_to_shipment, update_shipment_status, shipment_delete,finish_shipment
)

app_name = 'shipment'

urlpatterns = [
    path('', shipment_list, name='shipment_list'),
    path('create/', shipment_create, name='shipment_create'), #responsive
    path('<int:shipment_id>/', shipment_detail, name='shipment_detail'), #responsive
    path('<int:shipment_id>/add-product/', add_product_to_shipment, name='add_product_to_shipment'),
    path('<int:shipment_id>/finish/', finish_shipment, name='finish_shipment'), 
    path('update-shipment-status/<int:shipment_id>/', update_shipment_status, name='update_shipment_status'),
    path('<int:shipment_id>/delete/', shipment_delete, name='shipment_delete'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('<int:shipment_id>/edit-product/<int:item_id>/', views.edit_product, name='edit_product'),
    path('<int:shipment_id>/delete-product/<int:item_id>/', views.delete_product, name='delete_product'),
]