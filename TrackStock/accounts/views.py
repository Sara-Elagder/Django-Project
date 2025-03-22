from django.urls import reverse_lazy  
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, CreateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from inventory.models import Category, Product
from orders.models import Order, Supermarket
from shipment.models import Shipment
from accounts.forms import CustomUserCreationForm
from django.views.decorators.cache import never_cache
from .models import User
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

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
    context = {
        'total_employees': User.objects.filter(role='employee').count(),
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_orders': Order.objects.count(),
        'total_shipments': Shipment.objects.count(),
        'total_supermarkets': Supermarket.objects.count(),
        'total_managers': User.objects.filter(role='manager').count(),
    }
    return render(request, 'main_dashboard.html', context)