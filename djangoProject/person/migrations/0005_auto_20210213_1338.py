# Generated by Django 3.1.6 on 2021-02-13 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_person_slugname'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='firstNameCn',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='person',
            name='lastNameCn',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='firstName',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='lastName',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
