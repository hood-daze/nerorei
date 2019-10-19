# Generated by Django 2.2.6 on 2019-10-09 23:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=20)),
                ('message', models.TextField(max_length=4000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('has_bestAnser', models.BooleanField(default=False)),
                ('starter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tag', models.ManyToManyField(related_name='question_tag', to='tags.Tag', verbose_name='タグ全て')),
                ('tag1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_tag1', to='tags.Tag', verbose_name='タグ1')),
                ('tag2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_tag2', to='tags.Tag', verbose_name='タグ2')),
            ],
        ),
    ]
