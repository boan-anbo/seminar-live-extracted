# Generated by Django 3.1.6 on 2021-02-20 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='slugName',
            field=models.CharField(blank=True, default='', max_length=2000),
        ),
    ]
