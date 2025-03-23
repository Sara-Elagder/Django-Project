from django.urls import reverse_lazy  
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, CreateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from inventory.models import Category, Product
from orders.models import Order, Supermarket
from shipment.models import Shipment, ShipmentItem
from accounts.forms import CustomUserCreationForm
from django.views.decorators.cache import never_cache
from .models import User
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
import json
from datetime import datetime, timedelta
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from orders.models import OrderItem

class RegisterView(UserPassesTestMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'forms/registration_form.html'
    success_url = reverse_lazy('accounts:login')
    def test_func(self):
        return self.request.user.role == 'manager'
    def handle_no_permission(self):
        return redirect('accounts:login')

class LoginView(FormView):
    template_name = 'forms/login_form.html'  
    form_class = AuthenticationForm
    success_url = reverse_lazy('inventory:product_list')  

    @method_decorator(never_cache)  
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  
            return redirect(self.success_url)  
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.success_url)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')

class ManagerManagementView(UserPassesTestMixin, View):
    template_name = 'manager_management.html'
    def test_func(self):
        return self.request.user.role == 'manager'
    def handle_no_permission(self):
        return redirect('accounts:login')
    def get(self, request, *args, **kwargs):
        employees = User.objects.filter(role='employee')
        managers = User.objects.filter(role='manager').exclude(id=self.request.user.id)
        return render(request, self.template_name, {'employees': employees, 'managers': managers})
    def post(self, request, *args, **kwargs):
        if 'delete_employee' in request.POST:
            employee_id = request.POST.get('employee_id')
            employee = get_object_or_404(User, id=employee_id)
            employee.delete()
        elif 'delete_manager' in request.POST:
            manager_id = request.POST.get('manager_id')
            manager = get_object_or_404(User, id=manager_id)
            manager.delete()
        return redirect('accounts:manager_management')
    

class Custom404View(View):
    def get(self, request, exception=None):
        return render(request, '404.html', status=404)

def dashboard(request):
    # Categories: Number of products in each category
    categories = Category.objects.all()
    category_data = {category.name: Product.objects.filter(category=category).count() for category in categories}

    supermarkets_count = Supermarket.objects.count()
    employees_count = User.objects.filter(role='employee').count()
    orders_count = Order.objects.count()
    shipments_count = Shipment.objects.count()

    # Supermarket data with yearly comparison
    supermarkets = Supermarket.objects.all()
    current_year = datetime.now().year
    supermarket_data = {
        'labels': [market.name for market in supermarkets],
        'current_year': [Order.objects.filter(supermarket=market, date_created__year=current_year).count() for market in supermarkets],
        'previous_year': [Order.objects.filter(supermarket=market, date_created__year=current_year-1).count() for market in supermarkets]
    }

    # Employee data for scatter plot
    employees = User.objects.filter(role='employee')
    employee_data = [
        {
            'x': Order.objects.filter(created_by=emp).count(),  # Number of orders
            'y': OrderItem.objects.filter(order__created_by=emp).count(),  # Number of items
            'label': emp.username
        } for emp in employees
    ]

    # Orders by month and supermarket
    six_months_ago = datetime.now() - timedelta(days=180)
    supermarkets = Supermarket.objects.all()
    
    orders_by_month_and_supermarket = {}
    months_set = set()
    
    for supermarket in supermarkets:
        orders = Order.objects.filter(
            supermarket=supermarket,
            date_created__gte=six_months_ago
        ).annotate(
            month=TruncMonth('date_created')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        orders_by_month_and_supermarket[supermarket.name] = orders
        months_set.update(order['month'] for order in orders)
    
    months_list = sorted(list(months_set))
    
    orders_data = {
        'labels': [month.strftime('%B %Y') for month in months_list],
        'datasets': [
            {
                'label': supermarket.name,
                'data': [
                    next((o['count'] for o in orders_by_month_and_supermarket[supermarket.name] if o['month'] == month), 0)
                    for month in months_list
                ]
            }
            for supermarket in supermarkets
        ]
    }

    # Shipments data preparation - grouped by factory and month
    six_months_ago = datetime.now() - timedelta(days=180)
    factories_data = {}
    months_set = set()
    
    factories = Shipment.objects.values_list('factory_name', flat=True).distinct()
    
    for factory in factories:
        shipments = Shipment.objects.filter(
            factory_name=factory,
            date_received__gte=six_months_ago
        ).annotate(
            month=TruncMonth('date_received')
        ).values('month').annotate(
            total_items=Sum('items__quantity')
        ).order_by('month')
        
        factories_data[factory] = shipments
        months_set.update(ship['month'] for ship in shipments)
    
    months_list = sorted(list(months_set))
    
    shipments_data = {
        'labels': [month.strftime('%B %Y') for month in months_list],
        'datasets': [
            {
                'label': factory_name,
                'data': [
                    next((s['total_items'] for s in factories_data[factory_name] if s['month'] == month), 0)
                    for month in months_list
                ]
            }
            for factory_name in factories
        ]
    }

    context = {
        'total_employees': employees_count,
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_orders': orders_count,
        'total_shipments': shipments_count,
        'total_supermarkets': supermarkets_count,
        'total_managers': User.objects.filter(role='manager').count(),
        'category_data': json.dumps(category_data),  
        'supermarket_data': json.dumps(supermarket_data),
        'employee_data': json.dumps(employee_data),
        'orders_data': json.dumps(orders_data),
        'shipments_data': json.dumps(shipments_data),
    }
    return render(request, 'main_dashboard.html', context)