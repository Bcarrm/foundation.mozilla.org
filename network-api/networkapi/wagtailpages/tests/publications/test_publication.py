import http

from networkapi.wagtailpages.pagemodels.publications import publication
from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


class PublicationPageTests(test_base.WagtailpagesTestCase):
    def test_factory(self):
        publication_factory.PublicationPageFactory()

        self.assertTrue(True)

    def test_page_loads(self):
        publication_page = publication_factory.PublicationPageFactory(parent=self.homepage)

        response = self.client.get(path=publication_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, publication_page.title)
        self.assertTemplateUsed("wagtailpages/fragments/publication_hero.html")

    def test_page_loads_w_child(self):
        publication_page = publication_factory.PublicationPageFactory(parent=self.homepage)
        publication_factory.PublicationPageFactory(parent=publication_page)

        response = self.client.get(path=publication_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, publication_page.title)

    def test_page_loads_full_screen_hero(self):
        publication_page = publication_factory.PublicationPageFactory(
            parent=self.homepage,
            hero_layout=publication.PublicationPage.HERO_LAYOUT_FULL_SCREEN,
        )

        response = self.client.get(path=publication_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed("wagtailpages/fragments/custom_hero.html")
        self.assertTemplateNotUsed("wagtailpages/fragments/publication_hero.html")
