from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProductDetails(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.CharField(max_length=100)
    file_name = models.CharField(max_length=200)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

class Collections(models.Model):
    email = models.CharField(max_length=50)
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)