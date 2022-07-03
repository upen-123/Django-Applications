from cattle.models import Cattle, CattleDevice
from alert_engine.models import CattleAlert, BaseAlert
from microservice.api.schema import GetAllCattleSchema, CattleDeviceMappingSchema, CreateCattleActivityAlertSchema
from common.views import ResourceSystemView, api_exceptions
from django.http import JsonResponse
from notification.helpers import CattleAlertNotification
from alert_engine.helpers import ProcessAlert


class GetAllCattle(ResourceSystemView):
    schema_class = GetAllCattleSchema
    model = Cattle

    def get(self, request, *args, **kwargs):
        """
        @apiDescription Get all cattles and its created time
        This API would return the all cattles of active accounts present in db and it's created time. This API required basic authentication
         I.e Authorization -> Basic Auth -> username and password

        @api {get} api/v1/microservice/get-all-cattle/ Get All cattle

        @apiversion 1.0.0

        @apiName Get all Cattle
        @apiGroup Microservice

        @apiParam {String} [cattle_id] to retrieve activity data of a particular cattle_id


        @apiSuccessExample {json} Success-Response:
          HTTP/1.1 201 OK
          {
                 "response": {
                        "data": [
                           {
                                "cattle_id": "11e6c5bf-3033-4556-a0bc-218bc474e175",
                                "account_number": "7b7624",
                                "created_ts": "2019-11-14 18:28:29"
                            },
                            {
                                "cattle_id": "4066cda1-1760-4b28-b069-153f9083db96",
                                "account_number": "fde03d",
                                "created_ts": "2019-11-14 18:47:06"
                            },
                            {
                                "cattle_id": "a4b26fd8-7fa1-49a6-a840-71afecf690fd",
                                "account_number": "fde03d",
                                "created_ts": "2019-11-14 18:47:02"
                            },
                            {
                                "cattle_id": "d765e9b2-749d-4429-b8a4-8689cbbee8d2",
                                "account_number": "7b7624",
                                "created_ts": "2019-11-07 11:40:03"
                            }
                        ],
                        "messages": "Cattle information extracted successfully",
                        "status_code": 200
                        },
                        "meta": {}
          }

        @apiErrorExample {json} Error-Response: Invalid entry for cattle id

            {
                "message": "Bad request data.",
                "error": "{'cattle_id': ['Not a valid UUID.']}",
                "status_code": 400
            }

        @apiError   BadRequest Bad Request Data / Malformed request. 400
        @apiError   AuthenticationFailed Failed to Authenticate the user. 401
        @apiError   NotFound Not found 404
        @apiError   MethodNotAllowed method not allowed to access 405
        @apiError   ResourceInMutualExclusionZone Read/Write not allowed on the resource 409

        @apiError   (Error 5xx) ImproperlyConfigured Improperly Configured 500
        @apiError   (Error 5xx) ServiceUnavailable The server is currently unable to handle the request 503
        @apiError   (Error 5xx) NotImplemented Not Implemented 501

        """
        response = dict()
        cattle_id = self.req_params.get("cattle_id")
        if not cattle_id:
            cattle = self.model.objects.all()
            cattle_list = [
                {
                    "cattle_id": obj.id,
                    "account_number": obj.account.account_number,
                    "created_ts": obj.created_ts.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for obj in cattle
                if obj.account.is_active
            ]
        else:
            obj = self.model.objects.get(id=cattle_id)
            cattle_list = [{"cattle_id": obj.id, "created_ts": obj.created_ts.strftime("%Y-%m-%d %H:%M:%S")}]
        response["data"] = cattle_list
        response["messages"] = "Cattle information extracted successfully"
        response["status_code"] = 200
        return JsonResponse(self.make_response(response), status=200)


class GetCattleDeviceMapping(ResourceSystemView):
    schema_class = CattleDeviceMappingSchema
    model = CattleDevice

    def get(self, request, *args, **kwargs):
        """
        @apiDescription Get cattle device mapping
        This API would return the cattle and device mapping with cattle account created timestamp.
         I.e Authorization -> Basic Auth -> username and password

        @api {get} /api/v1/microservice/get-cattle-device/?cattle_id=73adcee2-7c73-4eb8-b6d6-13a809676d7b Get Cattle-Device Mapping

        @apiversion 1.0.0

        @apiName Get Cattle-Device Mapping
        @apiGroup Microservice

        @apiParam {String} [mac_id] Mac id
        @apiParam {String} [cattle_id] cattle id
        @apiParam {String} [start_time] start time
        @apiParam {string} [end_time] end time

        @apiSuccessExample {json} Success-Response:
          HTTP/1.1 201 OK
            {
                "response": {
                    "data": [
                        {
                            "mac_id": "31233326444",
                            "cattle_id": "73adcee2-7c73-4eb8-b6d6-13a809676d7b",
                            "account_number": "7b7624",
                            "device_id": "7f8c37c4-3a7e-4638-9508-272cf6c993a5",
                            "mapping_created_ts": "2019-05-29 14:51:40"
                        }
                    ],
                    "messages": "Cattle information extracted successfully",
                    "status_code": 200
                },
                "meta": {}
            }

        @apiError   BadRequest Bad Request Data / Malformed request. 400
        @apiError   AuthenticationFailed Failed to Authenticate the user. 401
        @apiError   NotFound Not found 404
        @apiError   MethodNotAllowed method not allowed to access 405
        @apiError   ResourceInMutualExclusionZone Read/Write not allowed on the resource 409

        @apiError   (Error 5xx) ImproperlyConfigured Improperly Configured 500
        @apiError   (Error 5xx) ServiceUnavailable The server is currently unable to handle the request 503
        @apiError   (Error 5xx) NotImplemented Not Implemented 501

        """
        response = dict()

        cattle_devices = self.model.get_cattle_device_mapping(
            mac_id=self.req_params.get("mac_id"),
            start_time=self.req_params.get("start_time"),
            end_time=self.req_params.get("end_time"),
            cattle_id=self.req_params.get("cattle_id"),
        )

        response["data"] = [
            {
                "mac_id": str(obj.device.mac_id),
                "cattle_id": str(obj.cattle.id),
                "account_number": str(obj.cattle.account.account_number),
                "device_id": str(obj.device.id),
                "cattle_name": obj.cattle.name,
                "cattle_tag_id": str(obj.cattle.cattle_tag_id),
                "mapping_created_ts": obj.created_ts.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for obj in cattle_devices
            if obj.cattle.account.is_active
        ]
        response["messages"] = "Cattle information extracted successfully"
        response["status_code"] = 200
        return JsonResponse(self.make_response(response), status=200)


class CreateCattleActivityAlert(ResourceSystemView):
    schema_class = CreateCattleActivityAlertSchema
    model = CattleAlert

    def post(self, request, *args, **kwargs):
        """
        @apiDescription Create activity alert for cattle.
        This API would create the activity alert status for cattle.

        @api {post} /api/v1/microservice/create-cattle-activity-alert/ Create Cattle Activity Alert

        @apiversion 1.0.0

        @apiName Create Cattle Activity Alert
        @apiGroup Microservice

        @apiParam {String} cattle_id cattle_id of cattle in system
        @apiParam {String} alert_warning_time alert_warning_time in system
        @apiParam {String} activity_status activity status (high/low)

        @apiParamExample {json} Request-Example:
        {
            "cattle_id" : "b258f3bb-640c-4506-9006-1d0edc0503ea",
            "alert_time" : "2019-07-09 12:54:44",
            "activity_status": "high",
        }

        @apiSuccessExample {json} Success-Response:
          HTTP/1.1 201 OK
          {
                "response": {
                    "message": "Cattle Activity alert created successfully",
                    "status_code": 201
                },
                "meta": {}
        }

        @apiError   BadRequest Bad Request Data / Malformed request. 400
        @apiError   AuthenticationFailed Failed to Authenticate the user. 401
        @apiError   NotFound Not found 404
        @apiError   MethodNotAllowed method not allowed to access 405
        @apiError   ResourceInMutualExclusionZone Read/Write not allowed on the resource 409

        @apiError   (Error 5xx) ImproperlyConfigured Improperly Configured 500
        @apiError   (Error 5xx) ServiceUnavailable The server is currently unable to handle the request 503
        @apiError   (Error 5xx) NotImplemented Not Implemented 501
        """

        response = dict()
        cattle = Cattle.objects.get(id=self.req_data["cattle_id"])

        alert = ProcessAlert(
            cattle_id=cattle.id,
            alert_time=self.req_data["alert_time"],
            activity_status=self.req_data["activity_status"],
        )

        if alert.validate_alert() and not alert.exist_generated_alerts():
            alert_name_obj = BaseAlert.get_alert(alert_name=alert.alert_name)

            if not alert_name_obj:
                raise api_exceptions.BadRequestData(errors="Alert name not matches with database.")

            self.req_data["alert"] = alert_name_obj[0]
            self.req_data.pop("activity_status")

            obj = self.model.objects.create(**self.req_data)

            alert_notify = CattleAlertNotification(
                cattle_id=cattle.id, alert_id=obj.id, account_id=cattle.account.id, flag_notify_group=True
            )

            alert_notify.notify_user_group(app_name=__package__.rsplit(".")[0], code="cattle_alert")

        response["message"] = "Cattle Activity Alert created successfully"
        response["status_code"] = 201
        return JsonResponse(self.make_response(response), status=201)
