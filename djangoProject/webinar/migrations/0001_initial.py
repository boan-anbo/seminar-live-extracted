# Generated by Django 3.1.5 on 2021-01-18 19:13

import uuid

import ckeditor.fields
import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lead', '0001_initial'),
        ('webinar_stat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isVisible', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('startDateTime', models.DateTimeField()),
                ('startDateTimeZone', models.CharField(default='UTC', max_length=100, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, default='')),
                ('duration', models.IntegerField(blank=True, default=120)),
                ('shortUrl', models.CharField(blank=True, max_length=255)),
                ('organization', models.CharField(blank=True, max_length=255)),
                ('originalUrl', models.CharField(blank=True, max_length=3000)),
                ('hasRecordingOrTranscript', models.BooleanField(default=False)),
                ('poster', models.FileField(blank=True, upload_to='posters')),
                ('extra', ckeditor.fields.RichTextField(blank=True)),
                ('requiresRegistration', models.BooleanField(blank=True, default=False)),
                ('requirement', models.CharField(blank=True, default='', max_length=280)),
                ('lead', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='webinar', to='lead.lead')),
                ('stat', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webinar_stat.webinarstat')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
