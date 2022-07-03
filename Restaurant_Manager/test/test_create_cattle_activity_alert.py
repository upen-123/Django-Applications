from cattle.tests.base import BaseCattleTestClass
import copy

from microservice.tests.base import call_endpoint_for_microservice


class CreateCattleActivityAlertRootTestCases(BaseCattleTestClass):
    """
    Create Cattle Activity Alert test cases
    """
    def setUp(self):
        """
        set up data step and sets endpoints
        :return:
        """
        super(CreateCattleActivityAlertRootTestCases,self).setUp()
        self.endpoint = "/api/v1/microservice/create-cattle-activity-alert/"
        self.method = "POST"
        self.dup_req_data = copy.deepcopy(self.req_data)
        self.token = self.root_token
        self.account_number = self.root_account
        self.create_cattle(self.account_number, self.token)
        self.duplicate_req_data = dict()
        self.duplicate_req_data["cattle_id"] = self.cattle_id
        self.duplicate_req_data["alert_time"] = "2019-07-09 12:54:44"
        self.duplicate_req_data["activity_status"] = "high"

    def test_create_cattle_activity_alert(self):
        """
        Test create cattle activity alert
        :return:
        """
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )

        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 201)

    def test_create_cattle_activity_alert_with_invalid_cattle_id(self):
        """
        Test create cattle activity alert with invalid cattle id
        :return:
        """

        self.duplicate_req_data["cattle_id"] = "048f021b-08c1-4b70-9f6a-a6ad116639"
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 400)
        self.assertEqual(create_cattle_activity_alert_resp["error"]["cattle_id"][0], "Not a valid UUID.")

    def test_create_cattle_activity_alert_with_missing_cattle_id(self):
        """
        Test Create cattle activity alert with missing cattle_id
        :return:
        """
        self.duplicate_req_data.pop("cattle_id")
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 400)
        self.assertEqual(create_cattle_activity_alert_resp["error"]["cattle_id"][0], "Missing data for required field.")

    def test_create_cattle_activity_alert_with_invalid_alert_time(self):
        """
        Test create cattle activity alert with invalid format of alert_time
        :return:
        """
        self.duplicate_req_data["alert_time"] = "2019-07-09"
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 400)
        self.assertEqual(create_cattle_activity_alert_resp["error"]["alert_time"][0], "Not a valid datetime.")

    def test_create_cattle_activity_alert_with_missing_alert_time(self):
        """
        Test create cattle activity alert with missing alert_time
        :return:
        """
        self.duplicate_req_data.pop("alert_time")
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 400)
        self.assertEqual(create_cattle_activity_alert_resp["error"]["alert_time"][0], "Alert Warning Time is required.")


    def test_create_cattle_activity_alert_with_invalid_activity_status(self):
        """
        Test create cattle activity alert with invalid activity status
        :return:
        """
        self.duplicate_req_data["activity_status"] = "abcdef"
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 400)
        self.assertEqual(create_cattle_activity_alert_resp["error"]["activity_status"][0], "Allowed values for activity_status is high/low")

    def test_create_cattle_activity_alert_with_missing_activity_status(self):
        """
        Test create cattle activity alert with missing activity-status
        :return:
        """
        self.duplicate_req_data.pop("activity_status")
        create_cattle_activity_alert_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(create_cattle_activity_alert_resp["status_code"], 400)
        self.assertEqual(create_cattle_activity_alert_resp["error"]["activity_status"][0], "Missing data for required field.")

    def test_create_cattle_activity_alert_with_invalid_credentials(self):
        """
        Test create cattle activity alert with invalid credentials
        :return:
        """
        self.duplicate_req_data["cattle_id"] = self.cattle_id
        get_cattle_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data = self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!',
            method=self.method
        )

        self.assertEqual(get_cattle_resp.status_code, 401)

