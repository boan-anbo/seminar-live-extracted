# Generated by Django 3.1.6 on 2021-02-08 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='isAnonymous',
            field=models.BooleanField(default=False),
        ),
    ]
