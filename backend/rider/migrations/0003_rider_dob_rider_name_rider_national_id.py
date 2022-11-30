# Generated by Django 4.1.3 on 2022-11-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rider", "0002_orderrider_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="rider",
            name="dob",
            field=models.DateField(auto_created=True, blank=True, null=True),
        ),
        migrations.AddField(
            model_name="rider",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="rider",
            name="national_id",
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
