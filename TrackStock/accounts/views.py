from django.urls import reverse_lazy  
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView , CreateView , View
from django.contrib.auth.mixins import   UserPassesTestMixin
from accounts.forms import CustomAuthenticationForm
from .models import User
class RegisterView (UserPassesTestMixin ,CreateView):
    model = User 
    form_class =CustomAuthenticationForm
    template_name = 'forms/registration_form.html'
    success_url = reverse_lazy('accounts:login')
    def test_func(self):
        return self.request.user.role=='manager' # If the user is authenticated, they can't access this page only managers can access this page
    def handle_no_permission(self):
        return redirect('accounts:login')  # redjrect to login page IF user is not super user



class LoginView (FormView):
    template_name = 'forms/login_form.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('inventory:product_list') # redirect to hmae page after login
    def form_valid(self , form ):
        user = form.get_user()
        login(self.request , user)
        if user.role == 'manager':
            return redirect('inventory:product_list')
        elif user.role == 'employee':
            return redirect('shipment:shipment_list')
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Log the user out
        return redirect('accounts:login')  # Redirect to the login page