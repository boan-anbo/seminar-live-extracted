# Generated by Django 3.1.5 on 2021-01-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0003_auto_20210123_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='type',
            field=models.CharField(choices=[('EVENT', 'EVENT'), ('REGISTRATION', 'REGISTRATION'), ('DETAIL', 'DETAIL'), ('ATTACHMENT', 'ATTACHMENT'), ('CONTACT', 'CONTACT'), ('ORGANIZATION', 'ORGANIZATION'), ('RECORDING', 'RECORDING'), ('TRANSCRIPT', 'TRANSCRIPT')], max_length=100),
        ),
    ]
