# Generated by Django 3.1.6 on 2021-02-21 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0003_auto_20210220_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='sourceType',
            field=models.CharField(blank=True, choices=[('EVENTBRITE', 'EVENTBRITE'), ('HNET', 'HNET'), ('WEB', 'WEB')], default='EVENTBRITE', max_length=100),
        ),
    ]
