# Generated by Django 3.1.6 on 2021-02-04 18:29

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True),
        ),
    ]
