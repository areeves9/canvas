# Generated by Django 3.2 on 2022-05-30 01:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flavor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('ocpc', models.CharField(max_length=60, unique=True)),
                ('qr', models.URLField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('seed_company', models.JSONField(blank=True, null=True)),
                ('lineage', models.JSONField(blank=True, null=True)),
                ('genetics', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('users_like', models.ManyToManyField(blank=True, related_name='strains_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
