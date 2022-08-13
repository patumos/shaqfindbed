# Generated by Django 3.2.5 on 2021-07-18 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_bed_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='prefix',
            field=models.CharField(choices=[('นางสาว', 'นางสาว'), ('นาย', 'นาย'), ('นาง', 'นาง'), ('ด.ช.', 'เด็กชาย'), ('ด.ญ.', 'เด็กหญิง')], max_length=30, null=True),
        ),
    ]
