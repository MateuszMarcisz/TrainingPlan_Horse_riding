# Generated by Django 5.0.6 on 2024-06-14 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patataj', '0002_remove_trainingplan_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingplan',
            name='trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patataj.trainer'),
        ),
    ]
