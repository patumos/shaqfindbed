# Generated by Django 3.2.7 on 2021-09-06 06:18

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wellness', '0003_auto_20210906_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wellnessstore',
            name='close_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='wellnessstore',
            name='open_days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('sun', 'Sunday'), ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday')], max_length=27, null=True),
        ),
        migrations.AlterField(
            model_name='wellnessstore',
            name='open_time',
            field=models.TimeField(null=True),
        ),
    ]
