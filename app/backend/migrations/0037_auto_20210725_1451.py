# Generated by Django 3.2.5 on 2021-07-25 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0036_auto_20210725_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='line_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='tel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='line_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='tel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
