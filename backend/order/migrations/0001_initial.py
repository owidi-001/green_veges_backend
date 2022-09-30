# Generated by Django 4.0.6 on 2022-09-30 05:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Un named', max_length=100)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('floor_number', models.IntegerField(blank=True, null=True)),
                ('door_number', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('rating', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Feedback',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('O', 'In Progress'), ('C', 'Cancelled'), ('F', 'Fulfilled')], db_index=True, default='P', max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='order date')),
                ('total', models.IntegerField()),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('T', 'On Transit'), ('C', 'Cancelled'), ('D', 'Delivered')], db_index=True, default='R', max_length=1)),
                ('timestamp', models.DateField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]
