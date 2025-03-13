from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import registrationForm
from .models import User

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'Manager'
    
    def handle_no_permission(self):
        return redirect('product_list')  # Redirect unauthorized users to a safe page

class RegistrationView(ManagerRequiredMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = registrationForm
    template_name = 'accounts/forms/registration_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'Employee'  # Use capitalized 'Employee' to match model definition
        user.save()
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/forms/login_form.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:  # Ensure user is logged in before accessing role
            if user.role == 'Manager':
                return reverse_lazy('employee_list')
            elif user.role == 'Employee':
                return reverse_lazy('product_list')
        return super().get_success_url()
