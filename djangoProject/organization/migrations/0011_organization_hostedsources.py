# Generated by Django 3.1.6 on 2021-02-20 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
        ('organization', '0010_organization_hostedleads'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='hostedSources',
            field=models.ManyToManyField(blank=True, related_name='hostOrganizations', to='sources.Source'),
        ),
    ]
