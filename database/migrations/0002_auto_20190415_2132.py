# Generated by Django 2.1.3 on 2019-04-15 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
        migrations.AddField(
            model_name='notification',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Device'),
        ),
    ]