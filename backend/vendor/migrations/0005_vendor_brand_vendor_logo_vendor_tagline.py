# Generated by Django 4.0.6 on 2022-09-21 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_remove_helpmessage_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='brand',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='logo',
            field=models.ImageField(null=True, upload_to='vendors/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='tagline',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
