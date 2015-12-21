#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_application import MockApplication

import mysql.connector
from mysql.connector import Error
from time import gmtime, strftime

@pytest.fixture(scope='function')
def mozwebqa_devhub_logged_in(request):
    from pages.desktop.developer_hub.home import Home
    mozwebqa = request.getfuncargvalue('mozwebqa')
    dev_home = Home(mozwebqa)
    dev_home.go_to_developers_homepage()
    dev_home.login(mozwebqa, user="default")

    return mozwebqa


@pytest.fixture(scope='function')
def free_app(request):
    """Return a free app created via the Marketplace API, and automatically delete the app after the test."""
    mozwebqa = request.getfuncargvalue('mozwebqa')
    request.app = MockApplication()
    api = MarketplaceAPI.get_client(mozwebqa.base_url,
                                    mozwebqa.credentials)
    api.submit_app(request.app)

    # This acts like a tearDown, running after each test function
    def fin():
        # If the app is being deleted by the test, set the id to 0
        if hasattr(request, 'app') and request.app['id'] > 0:
            api.delete_app(request.app)
    request.addfinalizer(fin)
    return request.app

@pytest.fixture(autouse=True)
def session_id(mozwebqa):
    print 'Session ID: {}'.format(mozwebqa.selenium.session_id)
    str = '{}\n'.format(mozwebqa.selenium.session_id)
    str_session_id = '{}'.format(mozwebqa.selenium.session_id)

    with open ("/home/adi/python.txt", "a") as myfile:
        myfile.write(str)

    current_time = strftime("%Y-%m-%d %H:%M")
    print('Current time is: {}'.format(current_time))
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='fireplace_sessionIDs',
                                       user='root',
                                       password='')
        if conn.is_connected():
            print('Connected to MySQL database')

        c = conn.cursor()
        tblQuery = """CREATE TABLE IF NOT EXISTS test_session_ids (id int unsigned auto_increment not NULL,
        session_id VARCHAR(60) not NULL,
        date_created VARCHAR(100) not NULL,
        primary key(id))"""
        c.execute(tblQuery)
        print('............Successfully created table .......')
        insQuery = """insert into test_session_ids (session_id, date_created) values ('%s', '%s')"""
        # insQuery = """insert into test_session_ids (session_id, date_created) values ('whatever', 'whatever')"""
        c.execute("insert into test_session_ids (session_id, date_created) values (%s, %s)", (str_session_id, current_time))
        # c.execute(insQuery)
        print('............Successfully ADDED to table .......')
        conn.commit()

    except Error as e:
        print(e)

    finally:
        conn.close()

