# Generated by Django 3.2.5 on 2021-08-01 06:18

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20210730_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_quill.fields.QuillField(default=None),
            preserve_default=False,
        ),
    ]
