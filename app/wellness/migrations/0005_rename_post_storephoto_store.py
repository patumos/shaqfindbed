# Generated by Django 3.2.7 on 2021-09-11 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wellness', '0004_auto_20210906_1318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storephoto',
            old_name='post',
            new_name='store',
        ),
    ]
