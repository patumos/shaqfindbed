# Generated by Django 3.2.5 on 2021-07-21 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_auto_20210721_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='directions',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='points',
            name='distance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Distance (km)'),
        ),
    ]
