# Generated by Django 4.2.4 on 2023-10-12 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_rename_organization_id_employeeeducation_organization_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Organisation',
            new_name='Organization',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='organisation_name',
            new_name='organization_name',
        ),
    ]