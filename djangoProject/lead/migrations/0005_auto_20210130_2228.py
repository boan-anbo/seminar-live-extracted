# Generated by Django 3.1.5 on 2021-01-30 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0004_auto_20210130_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='url',
            field=models.URLField(blank=True, default='', max_length=1000, unique=True),
        ),
    ]