# Generated by Django 3.2.5 on 2021-07-18 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20210718_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambulance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('license_plate', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('model_name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('working', 'Working'), ('free', 'Free'), ('ma', 'MA')], max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('idcard', models.CharField(max_length=20, null=True)),
                ('prefix', models.CharField(choices=[('นางสาว', 'นางสาว'), ('นาย', 'นาย'), ('นาง', 'นาง'), ('ด.ช.', 'เด็กชาย'), ('ด.ญ.', 'เด็กหญิง')], max_length=30, null=True)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=30, null=True)),
                ('photo', models.FileField(blank=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Photo')),
                ('address', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]