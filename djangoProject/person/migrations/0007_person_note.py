# Generated by Django 3.1.7 on 2021-02-28 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0006_remove_person_participant_webinars'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='note',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
