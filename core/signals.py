from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomUser

def connect_signals():
    @receiver(post_save, sender=User)
    def create_custom_user(sender, instance, created, **kwargs):
        if created:
            CustomUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_custom_user(sender, instance, **kwargs):
        instance.customuser.save()