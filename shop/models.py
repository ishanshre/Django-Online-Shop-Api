from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

# Product Database Model
class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=MinValueValidator(1))
    inventory = models.IntegerField(validators=MinValueValidator(0))
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


# Customer Database Model
class Customer(models.Model):
    class MEMBERSHIPS_CHOICES(models.TextChoices):
        MEMBERSHIP_BRONZE = 'B', 'Bronze'
        MEMBERSHIP_SILVER = 'S', 'Silver'
        MEMBERSHIP_GOLD = 'G', 'Gold'
        MEMBERSHIP_PLATINUM = 'P', 'Platinum'


    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=20, choices=MEMBERSHIPS_CHOICES.choices, default=MEMBERSHIPS_CHOICES.MEMBERSHIP_BRONZE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name','last_name']



# Order Database Model
class Order(models.Model):
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETE = 'P', 'Complete'
        FAILED = 'P', 'Failed'
        CANCELED = 'P', 'Canceled'
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} --> order status --> {self.payment_status}"
    