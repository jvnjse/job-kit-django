# Generated by Django 4.2.4 on 2023-10-26 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_remove_company_company_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='company_logo'),
        ),
    ]
