# Generated by Django 3.1.6 on 2021-02-04 15:19

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_organization_organization_hosts'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True),
        ),
    ]