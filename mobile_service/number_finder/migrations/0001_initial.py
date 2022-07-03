# Generated by Django 3.0.6 on 2022-05-22 09:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
            ],
        ),
    ]