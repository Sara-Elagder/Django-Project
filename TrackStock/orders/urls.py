from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('supermarket/create/', views.create_supermarket, name='create_supermarket'),
    path('list/', views.order_list, name='order_list'),
    path('supermarket/list/', views.supermarket_list, name='supermarket_list'),
]