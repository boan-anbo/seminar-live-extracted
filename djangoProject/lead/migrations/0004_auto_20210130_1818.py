# Generated by Django 3.1.5 on 2021-01-30 17:18

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0003_auto_20210125_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]