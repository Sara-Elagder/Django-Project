from django.urls import path
from .views import registrationView,UserLoginView

app_name = 'accounts'

urlpatterns = [
    path('register/', registrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
]