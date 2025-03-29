from django.db import migrations

def populate_citizenship(apps, schema_editor):
    # Get the Citizenship model from the apps registry
    Citizenship = apps.get_model('EligibleChecker', 'Citizenship')

    # List of countries to populate
    countries = [
        'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde',
        'Chad', 'Comoros', 'Congo (Democratic Republic)', 'Congo (Republic)', 'Djibouti', 'Egypt', 'Eswatini',
        'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho',
        'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique',
        'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa',
        'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
    ]

    # Create Citizenship entries for each country
    for country in countries:
        Citizenship.objects.create(name=country)

class Migration(migrations.Migration):

    dependencies = [
        ('EligibleChecker', '0001_initial'),  # Replace with the latest migration if necessary
    ]

    operations = [
        migrations.RunPython(populate_citizenship),
    ]