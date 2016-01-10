# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urlparse import urlparse

from fxapom.fxapom import DEV_URL, FxATestAccount, PROD_URL
import pytest
import MySQLdb
from time import gmtime, strftime
from mocks.marketplace_api import MarketplaceAPI
from mocks.mock_application import MockApplication


@pytest.fixture
def fxa_test_account(mozwebqa):
    prod_hosts = ['marketplace.firefox.com', 'marketplace.allizom.org']
    api_url = PROD_URL if urlparse(mozwebqa.base_url).hostname in prod_hosts else DEV_URL
    return FxATestAccount(api_url)


@pytest.fixture
def new_user(fxa_test_account):
    return {'email': fxa_test_account.email,
            'password': fxa_test_account.password,
            'name': fxa_test_account.email.split('@')[0]}


@pytest.fixture
def stored_users(variables):
    return variables['users']


@pytest.fixture
def existing_user(stored_users):
    return stored_users['default']


@pytest.fixture
def api(existing_user, mozwebqa):
    host = urlparse(mozwebqa.base_url).hostname
    key = existing_user['api'][host]['key']
    secret = existing_user['api'][host]['secret']
    return MarketplaceAPI(key, secret, host)


@pytest.fixture
def free_app(request, api):
    """Return a free app created via the Marketplace API, and automatically delete the app after the test."""
    app = MockApplication()
    api.submit_app(app)

    def fin():
        if app['id'] > 0:
            api.delete_app(app)
    request.addfinalizer(fin)
    return app

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
        conn = MySQLdb.connect(host='localhost',
                               user='root',
                               passwd='',
                               db='fireplace_sessionIDs')
        # if conn.is_connected():
        #         print('Connected to MySQL database')

        c = conn.cursor()
        tblQuery = """CREATE TABLE IF NOT EXISTS test_session_ids (id int unsigned auto_increment not NULL,
            session_id VARCHAR(60) not NULL,
            date_created VARCHAR(100) not NULL,
            primary key(id))"""
        c.execute(tblQuery)
        print('............Successfully created table .......')
        insQuery = """insert into test_session_ids (session_id, date_created) values ('%s', '%s')"""
        # insQuery = """insert into test_session_ids (session_id, date_created) values ('whatever', 'whatever')"""
        c = conn.cursor()
        c.execute("insert into test_session_ids (session_id, date_created) values (%s, %s)", (str_session_id, current_time))
        # c.execute(insQuery)
        print('............Successfully ADDED to table .......')
        conn.commit()
    except:
        print ('UNABLE TO PERFORM DATABASE OPERATION')

    finally:
        conn.close()