# Generated by Django 3.2.5 on 2021-07-18 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20210718_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='idcard',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='sex',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female')], max_length=30, null=True),
        ),
    ]
