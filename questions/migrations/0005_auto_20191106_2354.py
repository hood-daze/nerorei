# Generated by Django 2.2.6 on 2019-11-06 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20191015_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tag1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag2',
        ),
    ]
