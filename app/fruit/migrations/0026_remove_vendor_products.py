# Generated by Django 3.2.6 on 2021-08-09 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0025_vendorproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='products',
        ),
    ]