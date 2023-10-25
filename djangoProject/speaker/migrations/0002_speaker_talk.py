# Generated by Django 3.1.5 on 2021-01-18 19:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('speaker', '0001_initial'),
        ('talk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='talk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='talk.talk'),
        ),
    ]
