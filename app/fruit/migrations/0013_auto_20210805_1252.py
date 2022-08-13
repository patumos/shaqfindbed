# Generated by Django 3.2.6 on 2021-08-05 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0012_alter_photo_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='order_n',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='Photo'),
        ),
    ]