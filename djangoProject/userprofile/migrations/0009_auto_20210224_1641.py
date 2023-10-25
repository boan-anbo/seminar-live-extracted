# Generated by Django 3.1.7 on 2021-02-24 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_userprofile_istagger'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='isRecommender',
            field=models.BooleanField(default=False, verbose_name='Recommender status'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='isTagger',
            field=models.BooleanField(default=False, verbose_name='Tagger status'),
        ),
    ]