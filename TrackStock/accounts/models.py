from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class User(AbstractUser):
    EMPLOYEE = 'Employee'
    MANAGER = 'Manager'
    
    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (MANAGER, 'Manager'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)
    profile_image = models.ImageField(
        upload_to='accounts/profile_images/', 
        null=True, 
        blank=True, 
        default='accounts/profile_images/default_profile_image.png'
    )

    def __str__(self):
        return self.username

    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return static('accounts/img/default_profile_image.png')  # Uses Django's static function
