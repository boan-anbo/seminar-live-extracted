# Generated by Django 3.1.7 on 2021-03-02 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0011_auto_20210226_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='startDateTimeString',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
