# Generated by Django 3.2.5 on 2021-07-23 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_importfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='dest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.hospital'),
        ),
    ]
