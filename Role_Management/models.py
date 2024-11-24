from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length = 50)
    address = models.TextField()
    is_main = models.BooleanField(default = False)             # This is a field to check admin organiztion.

    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(max_length = 50)                    

    def __str__(self):
        return self.name
    
class User(AbstractUser):  
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE, null = True, blank = True, related_name = "organization")
    role = models.ForeignKey(Role, on_delete = models.CASCADE, null = True, blank = True, related_name = "role")
    objects = CustomUserManager()                        # Allows to use custom manager instead of default manager