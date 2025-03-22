from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.create_order, name='create_order'),
    path('supermarket/create/', views.create_supermarket, name='create_supermarket'),
    path("supermarket/<int:supermarket_id>/delete/", views.delete_supermarket, name="delete_supermarket"),
    path('supermarket/list/', views.supermarket_list, name='supermarket_list'),
    path('<int:order_id>/', views.order_details, name='order_details'),
    path('<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('<int:order_id>/delete-product/<int:item_id>/', views.delete_product, name='delete_product'),
    path('<int:order_id>/add-product/', views.add_product_to_order, name='add_product_to_order'),
    path("<int:order_id>/edit-product/<int:product_id>/", views.edit_product_in_order, name="edit_product_in_order"),
    path("<int:order_id>/change-status/", views.change_order_status, name="change_order_status"),
]