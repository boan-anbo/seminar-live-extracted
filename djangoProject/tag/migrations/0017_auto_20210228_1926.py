# Generated by Django 3.1.7 on 2021-02-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0016_tag_namepinyin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tagType',
            field=models.CharField(choices=[('LANGUAGE', 'Language'), ('DISCIPLINE', 'Discipline'), ('SUBFIELD', 'Subfield'), ('TOPIC', 'Topic'), ('AREA', 'Area')], default='TOPIC', max_length=255),
        ),
    ]
