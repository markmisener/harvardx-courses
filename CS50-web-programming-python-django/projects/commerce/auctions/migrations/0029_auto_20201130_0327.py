# Generated by Django 3.1.3 on 2020-11-30 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_auto_20201130_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('Clothing and Accessories', 'Clothing And Accessories'), ('Electronics and Games', 'Electronics And Games'), ('Other', 'Other'), ('None', ' ')], default='None', max_length=30),
        ),
    ]
