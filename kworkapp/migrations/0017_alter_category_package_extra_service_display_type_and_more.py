# Generated by Django 4.1.1 on 2022-10-02 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0016_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category_package_extra_service',
            name='display_type',
            field=models.CharField(blank=True, choices=[('number', 'Number'), ('boolean', 'Boolean'), ('extra_days', 'Extra Days'), ('extra_time', 'Extra Time'), ('none', 'None')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 20, 6, 59, 969997), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 20, 6, 59, 969997), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 20, 6, 59, 970998), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 20, 6, 59, 969997), null=True),
        ),
    ]
