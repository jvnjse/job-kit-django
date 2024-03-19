# Generated by Django 4.2.4 on 2023-10-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_remove_company_employee_company_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='company_website',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_sectors',
            field=models.ManyToManyField(blank=True, to='api.companysector'),
        ),
    ]