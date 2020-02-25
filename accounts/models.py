from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from programs.models import Department

# Create your models here.
class Profile(models.Model):
    USERTYPE_CHOICES = (
        ('0', 'Teacher'),
        ('1', 'Student'),
    )

    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic  = models.ImageField(upload_to="profile/%Y/%m/%d/",default="profile/default.png")
    phone_number = models.CharField(max_length=15,default='01xxxxxxxxxx')
    address      = models.TextField(default='Your Address')
    bio      = models.TextField(default='Your Bio')
    user_type = models.CharField(max_length=10, choices=USERTYPE_CHOICES, default="0")
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username



class Teacher(models.Model):
    teacher  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_teacher')
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='department_teacher')

    def __str__(self):
        return self.teacher.username


class Student(models.Model):
    student  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_student')

    def __str__(self):
        return self.student.username



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.user_profile.save()
    except Exception as e:
        pass