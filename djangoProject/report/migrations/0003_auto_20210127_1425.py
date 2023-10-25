# Generated by Django 3.1.5 on 2021-01-27 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_report_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='targetId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='targetType',
            field=models.CharField(blank=True, choices=[('WEBINAR', 'Webinar'), ('LINK', 'Link')], max_length=255, null=True),
        ),
    ]