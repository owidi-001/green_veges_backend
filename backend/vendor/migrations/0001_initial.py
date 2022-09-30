# Generated by Django 4.0.6 on 2022-09-30 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50, null=True)),
                ('logo', models.ImageField(null=True, upload_to='vendors/%Y/%m/%d/')),
                ('tagline', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HelpMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('upload', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vendor.vendor')),
            ],
        ),
    ]
