#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from tests.base_test import BaseTest
from pages.desktop.consumer_pages.home import Home


class TestConsumerPage(BaseTest):

    @pytest.mark.nondestructive
    def test_that_promo_module_is_visible(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.is_promo_box_visible)
        Assert.greater(home_page.promo_box_items_number, 0)

    @pytest.mark.sanity
    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_header_has_expected_items(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.true(home_page.header.is_logo_visible)
        Assert.true(home_page.header.is_search_visible)
        Assert.true(home_page.header.is_sign_in_visible)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_categories_menu(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        Assert.equal(home_page.categories.title, 'Categories')

        home_page.open_categories_menu()
        Assert.greater(len(home_page.categories.items), 0)

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_that_verifies_nav_menu_tabs(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.click_new_tab()
        Assert.equal('New', home_page.feed_title_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)

        home_page.click_popular_tab()
        Assert.equal('Popular', home_page.feed_title_text)
        Assert.true(home_page.apps_are_visible)
        Assert.true(home_page.elements_count > 0)
