# Generated by Django 3.2.13 on 2022-10-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0043_adds_listing_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='banneredcampaignpage',
            name='aside_page_content',
            field=models.BooleanField(default=False, help_text='Turning this on will create a right hand sidebar on large screens for any aside blocks added to the body.'),
        ),
    ]
