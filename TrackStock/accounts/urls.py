from django.conf.urls import handler404
from django.urls import path
from .views import Custom404View
from .views import RegisterView, LoginView, LogoutView, ManagerManagementView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

handler404 = Custom404View.as_view()
urlpatterns = [
     path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('manager-management/', ManagerManagementView.as_view(), name='manager_management'),
    path('dashboard/', views.dashboard, name='dashboard'),
]