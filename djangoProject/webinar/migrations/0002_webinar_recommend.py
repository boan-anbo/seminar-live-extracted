# Generated by Django 3.1.5 on 2021-01-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='recommend',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], default=0),
        ),
    ]
