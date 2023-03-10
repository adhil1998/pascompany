# Generated by Django 3.2 on 2022-12-24 14:23

import accounts.constants
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aadhar',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(choices=[(101, 'ADMIN'), (201, 'EXECUTIVE'), (301, 'SALESMAN')], default=accounts.constants.UserTypeChoices['SALESMAN']),
        ),
        migrations.CreateModel(
            name='ValidationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('add_info', models.JSONField(blank=True, default=dict, null=True, verbose_name='additional_info')),
                ('key', models.CharField(blank=True, default='', max_length=200)),
                ('status', models.IntegerField(choices=[(1, 'VTOKEN STATUS UNUSED'), (2, 'VTOKEN STATUS USED')], default=accounts.constants.VTokenStatusChoices['VTOKEN_STATUS_UNUSED'])),
                ('expiry', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.IntegerField(choices=[(1, 'VTOKEN TYPE SET PASS'), (2, 'VTOKEN TYPE RESET PASS'), (3, 'VTOKEN TYPE VERIFY EMAIL'), (4, 'VTOKEN TYPE OTP'), (5, 'VTOKEN TYPE MAGIC'), (6, 'VTOKEN TYPE CHANGE EMAIL'), (7, 'VTOKEN STATUS USED'), (8, 'VTOKEN TYPE VERIFY EMAIL OTP'), (9, 'VTOKEN TYPE RESET PASS OTP')], default=0)),
                ('creator', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator_validationtoken_objects', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updater_validationtoken_objects', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
    ]
