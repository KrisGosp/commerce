# Generated by Django 5.0.6 on 2024-07-04 11:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_listing_id_comment_listing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_winner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winning_bids', to=settings.AUTH_USER_MODEL),
        ),
    ]
