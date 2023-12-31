# Generated by Django 3.1.6 on 2021-02-17 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_remove_organization_organization_hosts'),
        ('host', '0007_host_host_leads'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='organizations',
            field=models.ManyToManyField(blank=True, related_name='organization_hosts', to='organization.Organization'),
        ),
    ]
