# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-23 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import networkapi.highlights.models
import wagtail.core.fields


class Migration(migrations.Migration):

    replaces = [
        ("highlights", "0001_initial"),
        ("highlights", "0002_auto_20170616_2032"),
        ("highlights", "0003_remove_highlight_featured"),
        ("highlights", "0004_highlight_homepage"),
        ("highlights", "0005_remove_highlight_homepage"),
        ("highlights", "0006_auto_20180208_2205"),
        ("highlights", "0007_nullify_homepage"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Highlight",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(help_text="Title of the higlight", max_length=300),
                ),
                (
                    "description",
                    models.TextField(help_text="Description of the higlight", max_length=5000),
                ),
                (
                    "link_label",
                    models.CharField(
                        help_text="Text to show that links to this higlight's details page",
                        max_length=300,
                    ),
                ),
                (
                    "link_url",
                    models.URLField(
                        help_text="Link to this higlight's details page",
                        max_length=2048,
                    ),
                ),
                (
                    "image",
                    models.FileField(
                        blank=True,
                        help_text="Image representing this highlight",
                        max_length=2048,
                        upload_to=networkapi.highlights.models.get_highlights_image_upload_path,
                    ),
                ),
                (
                    "footer",
                    wagtail.core.fields.RichTextField(
                        help_text="Content to appear after description (view more projects link or something similar)",
                        null=True,
                        verbose_name="footer",
                    ),
                ),
                (
                    "publish_after",
                    models.DateTimeField(
                        help_text="Make this highlight visible only after this date and time (UTC)",
                        null=True,
                    ),
                ),
                (
                    "expires",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        help_text="Hide this highlight after this date and time (UTC)",
                        null=True,
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(db_index=True, default=0, editable=False),
                ),
            ],
            options={
                "verbose_name_plural": "highlights",
                "ordering": ("order",),
            },
        ),
    ]
