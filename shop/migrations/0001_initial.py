# Generated by Django 5.1 on 2024-08-28 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=100, unique=True)),
                ('timezone_str', models.CharField(default='America/Chicago', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_id', models.CharField(max_length=100, unique=True)),
                ('uptime_last_hour', models.FloatField(default=0.0)),
                ('uptime_last_day', models.FloatField(default=0.0)),
                ('uptime_last_week', models.FloatField(default=0.0)),
                ('downtime_last_hour', models.FloatField(default=0.0)),
                ('downtime_last_day', models.FloatField(default=0.0)),
                ('downtime_last_week', models.FloatField(default=0.0)),
                ('status', models.CharField(default='Running', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('csv_file', models.FileField(blank=True, null=True, upload_to='reports/')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.store')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField()),
                ('start_time_local', models.TimeField()),
                ('end_time_local', models.TimeField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.store')),
            ],
        ),
        migrations.CreateModel(
            name='StoreStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_utc', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.store')),
            ],
        ),
    ]
