# Generated by Django 2.2.6 on 2019-10-12 09:18

import apiserver.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('file_url', models.URLField()),
                ('created_at', models.BigIntegerField(blank=True, default=apiserver.models.get_unixtimestamp, help_text='format: Unix timestamp')),
                ('md5', models.CharField(blank=True, max_length=16)),
                ('task_status', models.CharField(blank=True, choices=[('n', 'not exist'), ('r', 'running'), ('d', 'done'), ('e', 'error')], default='r', max_length=1)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
