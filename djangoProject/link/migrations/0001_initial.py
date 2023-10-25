# Generated by Django 3.1.5 on 2021-01-18 19:13

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('EVENT', 'EVENT'), ('REGISTRATION', 'REGISTRATION'), ('ATTACHMENT', 'ATTACHMENT'), ('CONTACT', 'CONTACT'), ('RECORDING', 'RECORDING'), ('TRANSCRIPT', 'TRANSCRIPT')], max_length=100)),
                ('note', models.CharField(blank=True, default='', max_length=280)),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
    ]
