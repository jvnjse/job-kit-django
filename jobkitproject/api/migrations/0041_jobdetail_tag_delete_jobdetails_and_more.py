# Generated by Django 4.2.4 on 2023-11-03 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_companysector_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('job_description', models.TextField()),
                ('qualifications_requirements', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('mode_of_work', models.CharField(choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Contract', 'Contract'), ('Remote', 'Remote')], max_length=20)),
                ('salary_range_from', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_range_to', models.DecimalField(decimal_places=2, max_digits=10)),
                ('application_deadline', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='JobDetails',
        ),
        migrations.AddField(
            model_name='jobdetail',
            name='keywords_tags',
            field=models.ManyToManyField(related_name='job_postings', to='api.tag'),
        ),
    ]
