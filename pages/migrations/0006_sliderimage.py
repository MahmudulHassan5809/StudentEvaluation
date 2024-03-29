# Generated by Django 2.2 on 2020-03-16 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0005_delete_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_image', models.ImageField(upload_to='slider/%Y/%m/%d/')),
                ('slider_title', models.CharField(max_length=255)),
                ('slider_description', models.TextField()),
            ],
        ),
    ]
