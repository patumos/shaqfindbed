# Generated by Django 3.2.6 on 2021-08-15 07:15

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0028_auto_20210809_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit.store'),
        ),
        migrations.AlterField(
            model_name='vendororder',
            name='product',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='vendor', chained_model_field='vendor', null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit.vendorproduct'),
        ),
    ]
