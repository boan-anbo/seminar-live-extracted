# Generated by Django 3.1.6 on 2021-02-10 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20210208_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='savedWebinars',
        ),
    ]
