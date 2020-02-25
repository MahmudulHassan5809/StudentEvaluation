from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models

# Create your models here.
class Semester(models.Model):
	semester_name = models.CharField(max_length=50)
	semester_year = models.CharField(max_length=50)
	semester_full_name = models.CharField(max_length=150)
	active = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		self.semester_full_name = self.semester_name + '_' + self.semester_year
		super(Semester, self).save(*args, **kwargs)

	def __str__(self):
		return self.semester_full_name



@receiver(post_save, sender=Semester)
def update_semester(sender, instance, created, **kwargs):
    if instance.active:
        all_semester = Semester.objects.all().exclude(id=instance.id)
        for semester in all_semester:
            semester.active = False
            semester.save()