# Generated by Django 4.2.4 on 2023-10-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_company_company_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address_line1',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]