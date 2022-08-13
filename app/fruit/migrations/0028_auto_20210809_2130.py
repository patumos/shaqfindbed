# Generated by Django 3.2.6 on 2021-08-09 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0027_auto_20210809_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fruit.buyer'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fruit.product'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fruit.store'),
        ),
    ]