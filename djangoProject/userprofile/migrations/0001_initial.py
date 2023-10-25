# Generated by Django 3.1.5 on 2021-01-18 19:13

import uuid

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currentView', models.CharField(default='TODAY', max_length=280)),
                ('timezone', models.CharField(blank=True, max_length=100)),
                ('showSavedOnly', models.BooleanField(default=False)),
                ('karma', models.IntegerField(default=5)),
                ('language', models.CharField(default='en', max_length=20)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
