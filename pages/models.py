from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class SliderImage(models.Model):
    slider_image = models.ImageField(upload_to="slider/%Y/%m/%d/")
    slider_title = models.CharField(max_length=255)
    slider_description = models.TextField()

    def __str__(self):
        return self.slider_title
