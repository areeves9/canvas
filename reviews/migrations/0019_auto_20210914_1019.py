# Generated by Django 3.2.5 on 2021-09-14 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0018_auto_20200520_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='method',
            field=models.CharField(choices=[('Flower', 'Flower'), ('Extract', 'Extract'), ('Edible', 'Edible')], default='Flower', max_length=20),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='user_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
