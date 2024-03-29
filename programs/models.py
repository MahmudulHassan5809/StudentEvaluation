from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models


class Faculty(models.Model):
    faculty_name = models.CharField(
        max_length=150, verbose_name='Department Name')

    class Meta():
        verbose_name = "Department"
        verbose_name_plural = "Department"

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name='faculty_department', verbose_name='Department Name')
    department_name = models.CharField(
        max_length=150, verbose_name='Program Name')

    class Meta():
        verbose_name = "Program"
        verbose_name_plural = "Program"

    def __str__(self):
        return self.department_name
