# Generated by Django 3.1.3 on 2020-11-27 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201126_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Clothing and Accessories', 'Clothing'), ('Electronics and Games', 'Electronics'), ('Other', 'Other')], default='Other', max_length=30),
        ),
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]