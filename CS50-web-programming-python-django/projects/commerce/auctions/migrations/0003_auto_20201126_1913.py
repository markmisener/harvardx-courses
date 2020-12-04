# Generated by Django 3.1.3 on 2020-11-26 19:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]