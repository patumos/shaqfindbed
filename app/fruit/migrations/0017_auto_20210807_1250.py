# Generated by Django 3.2.6 on 2021-08-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0016_auto_20210807_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sub_total',
        ),
        migrations.RemoveField(
            model_name='product',
            name='total',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vat',
        ),
        migrations.AddField(
            model_name='sale',
            name='sub_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='vat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
