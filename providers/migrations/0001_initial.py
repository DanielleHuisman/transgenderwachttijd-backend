# Generated by Django 3.2.6 on 2021-08-16 10:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('website', models.URLField(max_length=255)),
                ('scraped_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='providers.provider')),
            ],
        ),
    ]
