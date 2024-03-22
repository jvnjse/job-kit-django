# Generated by Django 5.0.3 on 2024-03-20 04:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='companysector',
            name='company_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='company_employee',
            name='employee_department',
        ),
        migrations.RemoveField(
            model_name='companydepartment',
            name='department_name',
        ),
        migrations.AddField(
            model_name='company_employee',
            name='employee_department',
            field=models.ManyToManyField(to='company.department'),
        ),
        migrations.AddField(
            model_name='companydepartment',
            name='department_name',
            field=models.ManyToManyField(to='company.department'),
        ),
    ]
