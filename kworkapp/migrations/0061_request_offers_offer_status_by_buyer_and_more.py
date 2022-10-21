# Generated by Django 4.0.8 on 2022-10-20 20:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0060_request_offers_offer_date_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='request_offers',
            name='offer_status_by_buyer',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('deleted', 'Removed')], default='active', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 20, 39, 56, 829925), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 20, 39, 56, 829925), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 20, 39, 56, 829925), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 20, 39, 56, 829925), null=True),
        ),
    ]