from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    