# Generated by Django 3.1.7 on 2021-02-25 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinar', '0019_auto_20210222_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='startDateTimeOriginal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]