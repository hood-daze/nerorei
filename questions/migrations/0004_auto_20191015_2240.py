# Generated by Django 2.2.6 on 2019-10-15 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='starter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
