# Generated by Django 2.2.6 on 2019-10-12 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0002_auto_20191012_0951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks',
            old_name='file_url',
            new_name='url',
        ),
    ]
