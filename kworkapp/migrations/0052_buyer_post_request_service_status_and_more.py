# Generated by Django 4.1.1 on 2022-10-16 18:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0051_usersearchterms_user_id_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer_post_request',
            name='service_status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('paused', 'Paused'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='buyer_post_request',
            name='service_type',
            field=models.CharField(blank=True, choices=[('individual', 'Individual'), ('all', 'All')], default='all', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 18, 1, 28, 715709), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 18, 1, 28, 715709), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 18, 1, 28, 716710), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 18, 1, 28, 716710), null=True),
        ),
        migrations.AlterField(
            model_name='usergigsimpressions',
            name='user_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
