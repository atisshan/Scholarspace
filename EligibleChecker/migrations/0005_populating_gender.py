from django.db import migrations

def populate_gender(apps, schema_editor):
    Gender = apps.get_model('EligibleChecker', 'Gender')
    Gender.objects.bulk_create([
        Gender(name='Male'),
        Gender(name='Female'),
    ])

class Migration(migrations.Migration):
    dependencies = [
        ('EligibleChecker', '0004_gender_remove_scholarship_gender_scholarship_gender'),
    ]

    operations = [
        migrations.RunPython(populate_gender),
    ]