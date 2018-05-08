# Generated by Django 2.0.4 on 2018-05-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approved_zone',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('coordinates', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Child_Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Child')),
            ],
        ),
        migrations.CreateModel(
            name='Danger_zone',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('coordinates', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=10)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('activated', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=20)),
                ('county', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=26, unique=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Parent_Approved_zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_zone_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Approved_zone')),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='Parent_Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Child')),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='Parent_Danger_zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('danger_zone_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Danger_zone')),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='Parent_Noification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Notification')),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Parent')),
            ],
        ),
        migrations.AddField(
            model_name='child_device',
            name='device_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Device'),
        ),
    ]
