from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=200)

class AdminDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    store_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=200)