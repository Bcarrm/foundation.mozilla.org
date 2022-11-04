# Generated by Django 3.2.13 on 2022-08-09 13:01

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailpages', '0047_buyersguidepagefeaturedarticlerelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyersGuidePageFeaturedUpdateRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_update_relations', to='wagtailpages.buyersguidepage')),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailpages.update')),
            ],
            options={
                'abstract': False,
                'unique_together': {('translation_key', 'locale')},
            },
        ),
    ]