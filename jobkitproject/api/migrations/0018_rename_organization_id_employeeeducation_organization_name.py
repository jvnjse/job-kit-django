# Generated by Django 4.2.4 on 2023-10-12 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_employeeeducation_delete_employeeexperienceeducation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeeducation',
            old_name='organization_id',
            new_name='organization_name',
        ),
    ]
