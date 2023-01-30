import http

from django.contrib.auth.models import User
from django.urls import reverse
from wagtail.contrib.redirects.models import Redirect

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base
from wagtail.core.models import Locale


class PageRedirectTest(test_base.WagtailpagesTestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("admin-user", "admin@example.com", "password")
        self.client.force_login(self.user)
        self.article_page_under_home_page = publication_factory.ArticlePageFactory(
            parent=self.homepage, title="Home page article"
        )
        self.article_index_page = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=self.homepage, title="News index"
        )
        self.article_page_under_index_page = publication_factory.ArticlePageFactory(
            parent=self.article_index_page, title="News article"
        )
        self.article_page_under_index_page_old_path = self.article_page_under_index_page.url

        # Translate some pages
        self.fr_homepage = self.homepage.copy_for_translation(self.fr_locale)

        self.en_locale = Locale.objects.get(language_code="en")
        self.fr_locale = Locale.objects.get(language_code="fr")

        self.fr_article_page_under_home_page = self.article_page_under_home_page.copy_for_translation(self.fr_locale)
        self.fr_article_index_page = self.article_index_page.copy_for_translation(self.fr_locale)
        self.fr_article_page_under_index_page = self.article_page_under_index_page.copy_for_translation(self.fr_locale)

        self.fr_article_page_under_index_page_old_path = self.fr_article_page_under_index_page.url

    def test_page_loads(self):
        response = self.client.get(path=self.article_page_under_home_page.get_url())
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_page_move_creates_redirect(self):
        # Check there are no redirects yet
        self.assertFalse(Redirect.objects.all())
        # Move the article under the index page out under the home page.
        response = self.client.post(
            reverse("wagtailadmin_pages:move_confirm", args=(self.article_page_under_index_page.id, self.homepage.id)),
            follow=True,
        )
        # Check the 'Page moved' message to show it's been moved
        self.assertContains(response, f"Page &#x27;{self.article_page_under_index_page}&#x27; moved")
        self.assertTrue(Redirect.objects.all())
        redirect = Redirect.objects.first()
        # check the redirect
        # +'/' because old path doesn't store trailing slash
        self.assertEqual(redirect.old_path + "/", self.article_page_under_index_page_old_path)
        self.assertEqual(redirect.redirect_page_id, self.article_page_under_index_page.id)

    def test_page_move_creates_redirect_french(self):
        # Check there are no redirects yet
        self.assertFalse(Redirect.objects.all())
        # Move the article under the index page out under the home page.
        response = self.client.post(
            reverse("wagtailadmin_pages:move_confirm", args=(self.fr_article_page_under_index_page.id, self.fr_homepage.id)),
            follow=True,
        )
        # Check the 'Page moved' message to show it's been moved
        self.assertContains(response, f"Page &#x27;{self.fr_article_page_under_index_page}&#x27; moved")
        self.assertTrue(Redirect.objects.all())
        redirect = Redirect.objects.first()
        # check the redirect
        # +'/' because old path doesn't store trailing slash
        self.assertEqual(redirect.old_path + "/", self.fr_article_page_under_index_page_old_path)
        self.assertEqual(redirect.redirect_page_id, self.fr_article_page_under_index_page.id)
