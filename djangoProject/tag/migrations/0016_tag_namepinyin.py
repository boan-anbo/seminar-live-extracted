# Generated by Django 3.1.7 on 2021-02-23 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0015_tag_taggingrecords'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='namePinyin',
            field=models.CharField(default='', max_length=100),
        ),
    ]
