# Generated by Django 2.1.3 on 2019-06-11 12:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_auto_20190608_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 11, 15, 7, 41, 886859)),
        ),
    ]