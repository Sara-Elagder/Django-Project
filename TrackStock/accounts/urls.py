from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ManagerManagementView
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('manager-management/', ManagerManagementView.as_view(), name='manager_management'),
]