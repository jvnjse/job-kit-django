# Generated by Django 4.2.4 on 2023-10-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_employeeexperienceeducation_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeexperienceeducation',
            name='experience_education_document',
            field=models.FileField(upload_to=''),
        ),
    ]
