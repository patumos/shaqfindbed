# Generated by Django 3.2.5 on 2021-08-01 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_postphoto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postphoto',
            old_name='product',
            new_name='post',
        ),
    ]
