# Generated by Django 3.1.3 on 2020-11-29 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20201129_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.Listing'),
        ),
    ]