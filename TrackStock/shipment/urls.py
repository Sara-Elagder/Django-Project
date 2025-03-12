from django.urls import path
from . import views

app_name = 'shipment'

urlpatterns = [
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
]