# Generated by Django 3.1.7 on 2021-02-28 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_userprofile_isleadcollector'),
        ('webinar', '0025_webinar_recommended'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='createdWebinars', to='userprofile.userprofile'),
        ),
    ]
