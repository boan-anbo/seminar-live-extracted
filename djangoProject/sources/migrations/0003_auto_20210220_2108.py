# Generated by Django 3.1.6 on 2021-02-20 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0002_source_slugname'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='hostId',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='organizationId',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
