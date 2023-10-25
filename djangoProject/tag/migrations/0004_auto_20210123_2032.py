# Generated by Django 3.1.5 on 2021-01-23 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0003_auto_20210123_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tagDiscipline',
        ),
        migrations.AlterField(
            model_name='tag',
            name='tagType',
            field=models.CharField(choices=[('LANGUAGE', 'Language'), ('SUBJECT', 'Subject'), ('TOPIC', 'Topic')], default='SUBJECT', max_length=255),
        ),
    ]
