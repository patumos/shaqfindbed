# Generated by Django 3.2.5 on 2021-07-25 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0032_remove_points_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
