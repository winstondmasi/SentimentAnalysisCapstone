# Generated by Django 4.2.9 on 2024-03-24 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_goemotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goemotion',
            name='id',
        ),
        migrations.AlterField(
            model_name='goemotion',
            name='data_id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, unique=True),
        ),
    ]
