# Generated by Django 3.1.6 on 2021-02-10 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0007_auto_20210202_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='eventUrl',
            field=models.URLField(blank=True, default='', max_length=1000),
        ),
    ]
