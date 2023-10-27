# Generated by Django 4.2.4 on 2023-10-26 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_company_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=100, null=True)),
                ('employee_position', models.CharField(max_length=100, null=True)),
                ('employee_phone_number', models.CharField(max_length=20, null=True)),
                ('employee_email', models.CharField(max_length=50, null=True)),
                ('employee_department', models.CharField(max_length=255, null=True)),
                ('company_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.company')),
            ],
        ),
    ]
