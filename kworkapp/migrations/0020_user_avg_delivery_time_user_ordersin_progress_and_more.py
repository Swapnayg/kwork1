# Generated by Django 4.1.1 on 2022-10-03 09:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0019_category_package_details_helper_txt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avg_delivery_time',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ordersin_progress',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 3, 9, 49, 5, 119789), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 3, 9, 49, 5, 119789), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 3, 9, 49, 5, 120791), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 3, 9, 49, 5, 120791), null=True),
        ),
        migrations.AlterField(
            model_name='sellerlevels',
            name='level_name',
            field=models.CharField(blank=True, choices=[('level1', 'New or higher'), ('level2', 'Advanced or higher'), ('level3', 'Professional')], default='Basic', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='seller_level',
            field=models.CharField(blank=True, choices=[('level1', 'New or higher'), ('level2', 'Advanced or higher'), ('level3', 'Professional')], default='level1', max_length=200, null=True),
        ),
    ]
