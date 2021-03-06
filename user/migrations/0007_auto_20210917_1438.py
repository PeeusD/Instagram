# Generated by Django 3.2.4 on 2021-09-17 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210917_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('None', 'Prefer not to specify')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_private_account',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
