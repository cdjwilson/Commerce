# Generated by Django 4.0.3 on 2022-07-14 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
