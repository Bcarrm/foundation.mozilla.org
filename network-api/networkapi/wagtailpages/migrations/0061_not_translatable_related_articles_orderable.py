# Generated by Django 3.2.16 on 2022-10-24 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0060_buyersguidecampaignpage_donationmodal_relation'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='buyersguidearticlepagerelatedarticlerelation',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='buyersguidearticlepagerelatedarticlerelation',
            name='locale',
        ),
        migrations.RemoveField(
            model_name='buyersguidearticlepagerelatedarticlerelation',
            name='translation_key',
        ),
    ]
