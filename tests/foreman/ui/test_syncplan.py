"""
Test class for Sync Plan UI
"""

from datetime import datetime, timedelta
from ddt import data, ddt
from nose.plugins.attrib import attr
from robottelo.common.constants import SYNC_INTERVAL
from robottelo.common.decorators import bzbug
from robottelo.common.helpers import generate_string, generate_strings_list
from robottelo.ui.factory import make_org
from robottelo.ui.locators import locators
from robottelo.ui.session import Session
from tests.foreman.ui.baseui import BaseUI


@ddt
class Syncplan(BaseUI):
    """
    Implements Sync Plan tests in UI
    """

    org_name = None

    def setUp(self):
        super(Syncplan, self).setUp()
        # Make sure to use the Class' org_name instance
        if Syncplan.org_name is None:
            Syncplan.org_name = generate_string("alpha", 8)
            with Session(self.browser) as session:
                make_org(session, org_name=Syncplan.org_name)

    def configure_syncplan(self):
        """
        Configures sync plan in UI
        """
        self.login.login(self.katello_user, self.katello_passwd)
        self.navigator.go_to_select_org(self.org_name)
        self.navigator.go_to_sync_plans()

    @attr('ui', 'syncplan', 'implemented')
    @data({u'name': generate_string('alpha', 10),
           u'desc': generate_string('alpha', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('numeric', 10),
           u'desc': generate_string('numeric', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('alphanumeric', 10),
           u'desc': generate_string('alphanumeric', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('utf8', 10),
           u'desc': generate_string('utf8', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('html', 20),
           u'desc': generate_string('html', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('alpha', 10),
           u'desc': generate_string('alpha', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('numeric', 10),
           u'desc': generate_string('numeric', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('alphanumeric', 10),
           u'desc': generate_string('alphanumeric', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('utf8', 10),
           u'desc': generate_string('utf8', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('html', 20),
           u'desc': generate_string('html', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('alpha', 10),
           u'desc': generate_string('alpha', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('numeric', 10),
           u'desc': generate_string('numeric', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('alphanumeric', 10),
           u'desc': generate_string('alphanumeric', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('utf8', 10),
           u'desc': generate_string('utf8', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('html', 20),
           u'desc': generate_string('html', 10),
           u'interval': SYNC_INTERVAL['week']})
    def test_positive_create_1(self, test_data):
        """
        @Feature: Content Sync Plan - Positive Create
        @Test: Create Sync Plan with minimal input parameters
        @Assert: Sync Plan is created
        """

        self.configure_syncplan()
        self.syncplan.create(test_data['name'], description=test_data['desc'],
                             sync_interval=test_data['interval'])
        self.assertIsNotNone(self.products.search(test_data['name']))

    @bzbug("1082632")
    @attr('ui', 'syncplan', 'implemented')
    def test_positive_create_3(self):
        """
        @Feature: Content Sync Plan - Positive Create
        @Test: Create Sync plan with specified start time
        @Assert: Sync Plan is created with the specified time.
        @BZ: 1082632
        """

        locator = locators["sp.fetch_startdate"]
        plan_name = generate_string("alpha", 8)
        self.configure_syncplan()
        description = "sync plan create with start date"
        current_date = datetime.now()
        startdate = current_date + timedelta(minutes=10)
        starthour = startdate.strftime("%H")
        startminute = startdate.strftime("%M")
        # Formatting current_date to web-UI format "%b %d, %Y %I:%M:%S %p"
        # Removed zero padded hrs & mins as fetching via web-UI doesn't have it
        # Removed the seconds info as it would be too quick to validate via UI.
        fetch_starttime = startdate.strftime("%b %d, %Y %I:%M:%S %p").\
            lstrip("0").replace(" 0", " ").rpartition(':')[0]
        self.syncplan.create(plan_name, description, start_hour=starthour,
                             start_minute=startminute)
        self.assertIsNotNone(self.products.search(plan_name))
        self.syncplan.search(plan_name).click()
        self.syncplan.wait_for_ajax()
        # Removed the seconds info as it would be too quick to validate via UI.
        starttime_text = str(self.syncplan.wait_until_element(locator).text).\
            rpartition(':')[0]
        self.assertEqual(starttime_text, fetch_starttime)

    @attr('ui', 'syncplan', 'implemented')
    def test_positive_create_4(self):
        """
        @Feature: Content Sync Plan - Positive Create
        @Test: Create Sync plan with specified start date
        @Assert: Sync Plan is created with the specified date
        """

        locator = locators["sp.fetch_startdate"]
        plan_name = generate_string("alpha", 8)
        self.configure_syncplan()
        description = "sync plan create with start date"
        current_date = datetime.now()
        startdate = current_date + timedelta(days=10)
        startdate_str = startdate.strftime("%Y-%m-%d")
        # validating only for date
        fetch_startdate = startdate.strftime("%b %d, %Y %I:%M:%S %p").\
            rpartition(',')[0]
        self.syncplan.create(plan_name, description, startdate=startdate_str)
        self.assertIsNotNone(self.products.search(plan_name))
        self.syncplan.search(plan_name).click()
        self.syncplan.wait_for_ajax()
        startdate_text = str(self.syncplan.wait_until_element(locator).text).\
            rpartition(',')[0]
        self.assertEqual(startdate_text, fetch_startdate)

    @attr('ui', 'syncplan', 'implemented')
    @data(*generate_strings_list())
    def test_positive_update_1(self, plan_name):
        """
        @Feature: Content Sync Plan - Positive Update name
        @Test: Update Sync plan's name
        @Assert: Sync Plan's name is updated
        """

        new_plan_name = generate_string("alpha", 8)
        description = "update sync plan"
        self.configure_syncplan()
        self.syncplan.create(plan_name, description)
        self.assertIsNotNone(self.products.search(plan_name))
        self.syncplan.update(plan_name, new_name=new_plan_name)
        self.assertIsNotNone(self.products.search(new_plan_name))

    @attr('ui', 'syncplan', 'implemented')
    @data({u'name': generate_string('alpha', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('numeric', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('alphanumeric', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('utf8', 10),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('html', 20),
           u'interval': SYNC_INTERVAL['hour']},
          {u'name': generate_string('alpha', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('numeric', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('alphanumeric', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('utf8', 10),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('html', 20),
           u'interval': SYNC_INTERVAL['day']},
          {u'name': generate_string('alpha', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('numeric', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('alphanumeric', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('utf8', 10),
           u'interval': SYNC_INTERVAL['week']},
          {u'name': generate_string('html', 20),
           u'interval': SYNC_INTERVAL['week']})
    def test_positive_update_2(self, test_data):
        """
        @Feature: Content Sync Plan - Positive Update interval
        @Test: Update Sync plan's interval
        @Assert: Sync Plan's interval is updated
        """

        description = "delete sync plan"
        locator = locators["sp.fetch_interval"]
        self.configure_syncplan()
        self.syncplan.create(test_data['name'], description)
        self.assertIsNotNone(self.products.search(test_data['name']))
        self.syncplan.update(test_data['name'],
                             new_sync_interval=test_data['interval'])
        self.navigator.go_to_sync_plans()
        self.syncplan.search(test_data['name']).click()
        interval_text = self.syncplan.wait_until_element(locator).text
        self.assertEqual(interval_text, test_data['interval'])

    @attr('ui', 'syncplan', 'implemented')
    @data(*generate_strings_list())
    def test_positive_delete_1(self, plan_name):
        """
        @Feature: Content Sync Plan - Positive Delete
        @Test: Delete a Sync plan
        @Assert: Sync Plan is deleted
        """

        description = "delete sync plan"
        self.configure_syncplan()
        self.syncplan.create(plan_name, description)
        self.assertIsNotNone(self.products.search(plan_name))
        self.syncplan.delete(plan_name)
        self.assertIsNone(self.products.search(plan_name))
