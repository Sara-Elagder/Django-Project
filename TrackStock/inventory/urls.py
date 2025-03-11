from django.urls import path
from . import views

urlpatterns = [
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
    path('product-added/', views.product_added, name='product_added'),
]