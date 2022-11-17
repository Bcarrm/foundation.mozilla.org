from django.db import models
from django.template.defaultfilters import slugify
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)
from networkapi.wagtailpages.utils import get_default_locale


@register_snippet
class BlogPageTopic(TranslatableMixin, models.Model):
    name = models.CharField(max_length=50)

    title = models.TextField(
        blank=True,
        help_text="Optional title that will apear on the page and when topic page is shared. "
        'If not set, will default to "name" text.',
    )

    intro = RichTextField(
        features=base_rich_text_options,
        blank=True,
    )
    share_description = models.TextField(
        blank=True,
        help_text="Optional description that will apear when topic page is shared. "
        'If not set, will default to "intro" text.',
    )
    share_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Share Image",
        help_text="Optional image that will apear when topic page is shared.",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("intro"),
        FieldPanel("share_description"),
        ImageChooserPanel("share_image"),
    ]

    @classmethod
    def get_topics(cls):
        (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()
        choices = [
            (topic.name, topic.name)
            for topic in BlogPageTopic.objects.filter(locale_id=DEFAULT_LOCALE_ID).order_by("name")
        ]
        choices.insert(0, ("All", "All"))
        return choices

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Blog Page Topic"
        verbose_name_plural = "Blog Page Topics"
