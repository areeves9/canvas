# Generated by Django 3.2 on 2022-06-07 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strains', '0006_alter_strain_ocpc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strain',
            name='ocpc',
            field=models.CharField(max_length=160, unique=True),
        ),
    ]
