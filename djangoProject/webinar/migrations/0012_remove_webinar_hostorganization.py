# Generated by Django 3.1.6 on 2021-02-17 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webinar', '0011_auto_20210217_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webinar',
            name='hostOrganization',
        ),
    ]
