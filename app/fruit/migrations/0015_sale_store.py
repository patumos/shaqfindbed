# Generated by Django 3.2.6 on 2021-08-07 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0014_buyer_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='store',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='fruit.store'),
            preserve_default=False,
        ),
    ]
