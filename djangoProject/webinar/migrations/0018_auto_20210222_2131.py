# Generated by Django 3.1.7 on 2021-02-22 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_userprofile_istagger'),
        ('webinar', '0017_auto_20210221_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='lastTagged',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='webinar',
            name='lastTaggedBy',
            field=models.ManyToManyField(blank=True, related_name='taggedWebinars', to='userprofile.UserProfile'),
        ),
    ]
