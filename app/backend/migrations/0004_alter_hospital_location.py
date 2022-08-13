# Generated by Django 3.2.5 on 2021-07-17 15:54

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_hospital_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
