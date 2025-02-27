# Generated by Django 3.2.18 on 2023-05-17 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("wagtailpages", "0082_alter_buyersguidecalltoaction_link_target_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="researchregion",
            name="slug",
            field=models.SlugField(
                help_text="The slug is auto-generated from the name, but can be customized if needed. It needs to be unique per locale.",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="researchtopic",
            name="slug",
            field=models.SlugField(
                help_text="The slug is auto-generated from the name, but can be customized if needed. It needs to be unique per locale.",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="researchregion",
            unique_together={("translation_key", "locale"), ("locale", "slug")},
        ),
        migrations.AlterUniqueTogether(
            name="researchtopic",
            unique_together={("translation_key", "locale"), ("locale", "slug")},
        ),
    ]
