# Generated by Django 3.1.5 on 2021-01-23 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_tag_webinars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='TagSubject',
        ),
        migrations.AddField(
            model_name='tag',
            name='tagDiscipline',
            field=models.CharField(choices=[('PHILOSOPHY', 'Philosophy'), ('LITERATURE', 'Literature'), ('ART', 'Art'), ('POLITICS', 'Politics'), ('ECONOMICS', 'Economics'), ('LAW', 'Law'), ('SOCIOLOGY', 'Sociology'), ('ANTHROPOLOGY', 'Anthropology'), ('HISTORY', 'History')], default='PHILOSOPHY', max_length=255),
        ),
    ]