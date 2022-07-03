import copy
from cattle.tests.base import BaseCattleTestClass
from microservice.tests.base import call_endpoint_for_microservice

class GetAllCattleRootTestCases(BaseCattleTestClass):
    """
    Get All Cattle Test cases
    """

    def setUp(self):
        """
        set up data step and sets endpoints
        :return:
        """
        super(GetAllCattleRootTestCases,self).setUp()
        self.endpoint = "/api/v1/microservice/get-all-cattle/"
        self.method = "GET"
        self.dup_req_data = copy.deepcopy(self.req_data)
        self.token = self.root_token
        self.account_number = self.root_account
        self.create_cattle(self.account_number, self.token)
        self.duplicate_req_data = dict()
        self.duplicate_req_data["cattle_id"] = self.cattle_id

    def test_get_all_cattle_with_cattle_id(self):
        """
        Test get all cattle with cattle_id
        :return:
        """
        self.duplicate_req_data["cattle_id"] = self.cattle_id
        get_cattle_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data=self.duplicate_req_data,
            username= 'dashboard',
            password= 'dashboard@123!@',
            method=self.method
        )
        self.assertNotEqual(len(get_cattle_resp["data"]), 0)
        self.assertEqual(get_cattle_resp["status_code"], 200)


    def test_get_all_cattle_without_cattle_id(self):
        """
        Test get all cattle without cattle_id
        :return:
        """
        self.duplicate_req_data.pop("cattle_id")
        get_cattle_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data = self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertNotEqual(len(get_cattle_resp["data"]), 0)
        self.assertEqual(get_cattle_resp["status_code"], 200)

    def test_get_all_cattle_with_invalid_cattle_id(self):
        """
        Test get all cattle with invalid cattle_id
        :return:
        """
        self.duplicate_req_data["cattle_id"]="asadvjbjsjtyiasd"
        get_cattle_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data = self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(get_cattle_resp["error"]["cattle_id"][0],"Not a valid UUID.")
        self.assertEqual(get_cattle_resp["status_code"], 400)

    def test_get_all_cattle_with_blank_cattle_id(self):
        """
        Test get all cattle with blank cattle_id
        :return:
        """
        self.duplicate_req_data["cattle_id"]=""
        get_cattle_resp = call_endpoint_for_microservice(
            testclient=self.client,
            endpoint=self.endpoint,
            req_data = self.duplicate_req_data,
            username='dashboard',
            password='dashboard@123!@',
            method=self.method
        )
        self.assertEqual(get_cattle_resp["error"]["cattle_id"][0], "Not a valid UUID.")
        self.assertEqual(get_cattle_resp["status_code"], 400)

    def test_get_all_cattle_with_invalid_credentials(self):
        """
        Test get all cattle with invalid credentials
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

