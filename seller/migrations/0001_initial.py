# Generated by Django 4.1.5 on 2023-01-28 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('gst_no', models.CharField(max_length=15)),
            ],
        ),
    ]