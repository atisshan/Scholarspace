# Generated by Django 5.1.3 on 2025-02-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EligibleChecker', '0017_remove_university_description_university_campus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
    ]
