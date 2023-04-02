import typing
from typing import Optional

from django.core import paginator
from django.db import models
from django.utils.translation import pgettext_lazy
from wagtail import images as wagtail_images
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.images import edit_handlers as image_panels
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels import profiles as profile_models
from networkapi.wagtailpages.pagemodels.research_hub import base as research_base
from networkapi.wagtailpages.pagemodels.research_hub import (
    constants,
    detail_page,
    taxonomies,
)

if typing.TYPE_CHECKING:
    from django import http, template


class ResearchLibraryPage(research_base.ResearchHubBasePage):
    max_count = 1
    parent_page_types = ["ResearchLandingPage"]
    subpage_types = ["ResearchDetailPage"]

    banner_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    results_count = models.PositiveSmallIntegerField(
        default=10,
        help_text="Maximum number of results to be displayed per page.",
    )

    content_panels = research_base.ResearchHubBasePage.content_panels + [
        image_panels.FieldPanel("banner_image"),
    ]

    settings_panels = research_base.ResearchHubBasePage.settings_panels + [panels.FieldPanel("results_count")]

    translatable_fields = [
        # Content tab fields
        TranslatableField("title"),
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]

    def get_context(self, request: "http.HttpRequest") -> "template.Context":
        search_query: str = request.GET.get("search", "")
        sort_value: str = request.GET.get("sort", "")
        sort: constants.SortOption = constants.SORT_CHOICES.get(sort_value, constants.SORT_NEWEST_FIRST)
        filtered_author_ids: list[int] = [int(author_id) for author_id in request.GET.getlist("author")]
        filtered_topic_ids: list[int] = [int(topic_id) for topic_id in request.GET.getlist("topic")]
        filtered_region_ids: list[int] = [int(region_id) for region_id in request.GET.getlist("region")]
        # Because a research detail page can only have a single publication date, we
        # can also only select a single one. Otherwise we would filter for pages with
        # two publication dates which does not exist.
        year_parameter: str = request.GET.get("year", "")
        filtered_year: Optional[int]
        try:
            filtered_year = int(year_parameter)
        except ValueError:
            # Any non-number year parameter will trigger the ValueError.
            filtered_year = None
        page: Optional[str] = request.GET.get("page")

        searched_and_filtered_research_detail_pages = self._get_research_detail_pages(
            search=search_query,
            sort=sort,
            author_profile_ids=filtered_author_ids,
            topic_ids=filtered_topic_ids,
            region_ids=filtered_region_ids,
            year=filtered_year,
        )
        research_detail_pages_paginator = paginator.Paginator(
            object_list=searched_and_filtered_research_detail_pages,
            per_page=self.results_count,
            allow_empty_first_page=True,
        )
        research_detail_pages_page = research_detail_pages_paginator.get_page(page)

        context: "template.Context" = super().get_context(request)
        context["breadcrumbs"] = self.get_breadcrumbs()
        context["search_query"] = search_query
        context["sort"] = sort
        context["author_options"] = self._get_author_options()
        context["filtered_author_ids"] = filtered_author_ids
        context["topic_options"] = self._get_topic_options()
        context["filtered_topic_ids"] = filtered_topic_ids
        context["region_options"] = self._get_region_options()
        context["filtered_region_ids"] = filtered_region_ids
        context["year_options"] = self._get_year_options()
        context["filtered_year"] = filtered_year
        context["research_detail_pages_count"] = research_detail_pages_paginator.count
        context["research_detail_pages"] = research_detail_pages_page
        return context

    def _get_author_options(self):
        author_profiles = profile_models.Profile.objects.filter_research_authors()
        author_profiles = utils.localize_queryset(author_profiles)
        return [
            {
                "id": author_profile.id,
                "value": author_profile.id,
                "label": author_profile.name,
            }
            for author_profile in author_profiles
        ]

    def _get_topic_options(self):
        topics = taxonomies.ResearchTopic.objects.all()
        topics = utils.localize_queryset(topics)
        return [
            {
                "id": topic.id,
                "value": topic.id,
                "label": topic.name,
            }
            for topic in topics
        ]

    def _get_region_options(self):
        regions = taxonomies.ResearchRegion.objects.all()
        regions = utils.localize_queryset(regions)
        return [
            {
                "id": region.id,
                "value": region.id,
                "label": region.name,
            }
            for region in regions
        ]

    def _get_year_options(self):
        dates = detail_page.ResearchDetailPage.objects.dates(
            "original_publication_date",
            "year",
            order="DESC",
        )
        year_options = [
            {
                "id": date.year,
                "value": date.year,
                "label": date.year,
            }
            for date in dates
        ]
        empty_option = {
            "id": "any",
            "value": "",
            "label": pgettext_lazy("Option in a list of years", "Any"),
        }
        return [empty_option] + year_options

    def _get_research_detail_pages(
        self,
        *,
        search: str = "",
        sort: constants.SortOption = constants.SORT_NEWEST_FIRST,
        author_profile_ids: Optional[list[int]] = None,
        topic_ids: Optional[list[int]] = None,
        region_ids: Optional[list[int]] = None,
        year: Optional[int] = None,
    ):
        author_profile_ids = author_profile_ids or []
        topic_ids = topic_ids or []
        region_ids = region_ids or []

        research_detail_pages = detail_page.ResearchDetailPage.objects.live().public()
        research_detail_pages = research_detail_pages.filter(locale=wagtail_models.Locale.get_active())

        author_profiles = profile_models.Profile.objects.filter_research_authors()
        author_profiles = author_profiles.filter(id__in=author_profile_ids)
        for author_profile in author_profiles:
            # Synced but not translated pages are still associated with the default
            # locale's author profile. But, we want to show them when we are filtering
            # for the localized author profile. We use the fact that the localized and
            # default locale's author profile have the same `translation_key`.
            research_detail_pages = research_detail_pages.filter(
                research_authors__author_profile__translation_key=(author_profile.translation_key)
            )

        topics = taxonomies.ResearchTopic.objects.filter(id__in=topic_ids)
        for topic in topics:
            research_detail_pages = research_detail_pages.filter(
                related_topics__research_topic__translation_key=topic.translation_key
            )

        regions = taxonomies.ResearchRegion.objects.filter(id__in=region_ids)
        for region in regions:
            research_detail_pages = research_detail_pages.filter(
                related_regions__research_region__translation_key=region.translation_key
            )

        if year:
            research_detail_pages = research_detail_pages.filter(original_publication_date__year=year)

        research_detail_pages = research_detail_pages.order_by(sort.order_by_value)

        if search:
            research_detail_pages = research_detail_pages.search(
                search,
                order_by_relevance=False,  # To preserve original ordering
            )

        return research_detail_pages

    def get_banner(self):
        return self.banner_image
