# Generated by Django 3.1.6 on 2021-02-15 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20210215_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='orgNameCn',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='orgNameShort',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='organization',
            name='orgNameShortCn',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
