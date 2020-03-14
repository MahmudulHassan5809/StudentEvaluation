from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class City(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_weather')
    city = models.CharField(max_length=25)

    def __str__(self):
        return self.city


@receiver(post_save, sender=City)
def update_semester(sender, instance, created, **kwargs):
    all_city_count = City.objects.all().exclude(id=instance.id).count()
    all_city = City.objects.all().exclude(id=instance.id)
    if all_city_count > 1:
        for city in all_city:
            city.delete()
