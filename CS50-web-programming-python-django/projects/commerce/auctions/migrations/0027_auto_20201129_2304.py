# Generated by Django 3.1.3 on 2020-11-29 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_auto_20201129_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(blank=True, default="{% static 'auctions/imgs/generic-image-placeholder.png' %}", max_length=250),
        ),
    ]
