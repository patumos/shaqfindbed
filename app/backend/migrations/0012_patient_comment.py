# Generated by Django 3.2.5 on 2021-07-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20210718_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
