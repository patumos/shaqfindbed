# Generated by Django 3.2.5 on 2021-07-23 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0031_points_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='points',
            name='ticket',
        ),
    ]
