# Generated by Django 2.2.6 on 2019-10-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]