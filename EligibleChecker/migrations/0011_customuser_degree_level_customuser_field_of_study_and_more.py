# Generated by Django 5.1.3 on 2025-01-31 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EligibleChecker', '0010_alter_scholarship_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='degree_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EligibleChecker.degreelevel'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='field_of_study',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='EligibleChecker.gender'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='min_gpa',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='work_experience',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
