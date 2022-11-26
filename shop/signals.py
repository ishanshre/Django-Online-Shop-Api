from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from shop.models import Customer


User = get_user_model()

@receiver(signal=post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(signal=post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer_profile.save()



