# Generated by Django 4.1.1 on 2022-10-02 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0018_alter_category_package_extra_service_display_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category_package_details',
            name='helper_txt',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='category_package_extra_service',
            name='helper_txt',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 22, 3, 32, 526134), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 22, 3, 32, 526134), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 22, 3, 32, 527135), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 2, 22, 3, 32, 527135), null=True),
        ),
    ]
