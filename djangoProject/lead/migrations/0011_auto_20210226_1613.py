# Generated by Django 3.1.7 on 2021-02-26 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0010_lead_registrationdeadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='url',
            field=models.URLField(blank=True, default='', max_length=1000, null=True, unique=True),
        ),
    ]
