# Generated by Django 3.2.13 on 2022-06-17 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0028_topics_max_num_helptext"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="slug",
            field=models.SlugField(blank=True),
        ),
    ]
