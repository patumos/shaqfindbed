# Generated by Django 3.2.5 on 2021-07-18 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_ambulance_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbulanceTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('working', 'Working'), ('free', 'Free'), ('ma', 'MA')], max_length=30, null=True)),
                ('checkin_at', models.DateTimeField(blank=True, null=True)),
                ('checkout_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ambulance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.ambulance')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.driver')),
            ],
        ),
    ]