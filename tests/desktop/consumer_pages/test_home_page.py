# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from tests.base_test import BaseTest
from pages.desktop.consumer_pages.home import Home


class TestConsumerPage(BaseTest):

    @pytest.mark.sanity
    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_header_has_expected_items(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert home_page.header.is_logo_visible
        assert home_page.header.is_search_visible
        assert home_page.header.is_sign_in_visible

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        assert 'Categories' == home_page.header.categories_name
        assert home_page.header.categories_name == 'Categories'
        home_page.header.open_categories_menu()
        assert len(home_page.header.categories) > 0

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_opening_category_pages_from_categories_menu(self, mozwebqa):
        """Open the first 3 category pages and check the first 3 apps on those pages."""
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        # only check the first three categories (excluding games)
        for i in range(1, 4):
            home_page.header.open_categories_menu()
            category = home_page.header.categories[i]
            category_name = category.name
            category_page = category.click()
            assert category_name.title() == category_page.category_title
            assert category_page.is_the_current_page
            apps = category_page.apps
            assert len(apps) > 0
            assert category_page.is_new_popular_tabs_visible
            assert category_page.is_popular_tab_selected

            # only check the first three apps in the category
            for app in apps[:3]:
                assert app.is_name_visible
                assert app.is_icon_visible
                assert app.is_rating_visible
                assert app.is_install_visible

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_nav_menu_tabs(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()
        home_page.click_new_tab()
        assert 'New' in home_page.feed_title_text
        assert home_page.apps_are_visible
        assert home_page.elements_count > 0

        home_page.click_popular_tab()
        assert 'Popular' in home_page.feed_title_text
        assert home_page.apps_are_visible
        assert home_page.elements_count > 0
