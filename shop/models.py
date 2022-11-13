from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import uuid
# Create your models here.


#promotion  model
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

# Collection Model
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name="+", blank=True)
    # avoid circular relationship with plus sign in related name
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']


# Product Database Model
class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='collection_products', null=True, blank=True)
    promotions = models.ManyToManyField(Promotion, related_name='promotions_products', blank=True)
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

    class GENDER(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHERS = "O", "Others"


    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    birth_date = models.DateTimeField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices, blank=True)
    membership = models.CharField(max_length=20, choices=MEMBERSHIPS_CHOICES.choices, default=MEMBERSHIPS_CHOICES.MEMBERSHIP_BRONZE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['gender','membership']



# Order Database Model
class Order(models.Model):
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETE = 'C', 'Complete'
        FAILED = 'F', 'Failed'
        CANCELED = 'CA', 'Canceled'
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} --> order status --> {self.payment_status}"

    

# Order Items
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_orderitems')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])


# Address Model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


# cart model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)


# cart items model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems_product')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart','product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)], blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

