from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from number_finder.api.schema import PhoneNumberDetailsSchema
from number_finder.exceptions import api_exception_handler, BadRequestData

from number_finder.models import Users


class CreateUserDetail(View):
    """
    @apiDescription Registration of user

    @api {post} /number-finder/create-user/ Registration User


    @apiversion 1.0.0
    @apiName Registration User
    @apiGroup NumberFinder


    @apiParam {String} name name of the user
    @apiParam {String} phone_number phone number of the user
    @apiParam {String} password password of the user
    @apiParam {Number} [email] email of the user

    @apiSuccessExample {json} Success-Response:Based on without account number

      HTTP/1.1 200 OK

      {
        "payload": {
            "message": "User has been registered successfully.",
            "status_code": 201
    }
   }

    """
    schema = PhoneNumberDetailsSchema()
    model = Users

    @method_decorator(api_exception_handler)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateUserDetail, self).dispatch(request, **kwargs)

    def post(self, request, *args, **kwargs):
        data, errors = self.schema.loads(request.body)
        if errors:
            raise BadRequestData(errors=errors)

        email = data.pop("email") if "email" in data else None
        password = data.pop("password")
        self.model.objects.create_user(email=email, password=password, **data)
        response = dict()
        response["payload"] = {
            "message": "User has been registered successfully.", "status_code": 201
        }
        return JsonResponse(response)


class GetPhoneNumberDetail(View):

    """
        @apiDescription Registration of user

        @api {post} /number-finder/get-user/ Get User Details


        @apiversion 1.0.0
        @apiName Get User Details
        @apiGroup NumberFinder

        @apiParam {String} phone_number phone number of the user

        @apiSuccessExample {json} Success-Response:

          HTTP/1.1 200 OK

{
    "payload": [
        [
            {
                "user_id": "cf0ce2f3-0eb2-4960-a05d-3df307028ddd",
                "phone_number": "7682234524",
                "name": "Ram",
                "email": "",
                "is_user_spam": false
            }
        ],
        {}
    ],
    "message": "user details has been fetched successfully."
}

        """

    schema = PhoneNumberDetailsSchema()
    model = Users

    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.filter(phone_number=request.GET.get("phone_number"))
        response = dict(payload=self.schema.dump(queryset, many=True))
        response["message"] = "user details has been fetched successfully."
        return JsonResponse(response)


class UpdatePhoneNumberDetail(View):
    """
        @apiDescription Registration of user

        @api {post} /number-finder/update-user/<user_id>/ Update User


        @apiversion 1.0.0
        @apiName Update User
        @apiGroup NumberFinder


        @apiParam {Boolean} is_spam if user want to make some number spam

        @apiSuccessExample {json} Success-Response:

          HTTP/1.1 200 OK

          {
            "payload": {
                "message": "User has been updated successfully.",
                "status_code": 202
        }
       }

        """
    schema = PhoneNumberDetailsSchema()
    model = Users

    @method_decorator(api_exception_handler)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdatePhoneNumberDetail, self).dispatch(request, **kwargs)

    def put(self, request, *args, **kwargs):
        data, errors = self.schema.loads(request.body, partial=True)
        if errors:
            raise BadRequestData(errors=errors)
        if data.get("is_spam"):
            user = self.model.objects.filter(id=kwargs["id"]).first()
            if not user:
                raise BadRequestData(errors="User not exist in system.")

            user.spam_count += 1
            user.save()

        response = dict()
        response["payload"] = {
            "message": "User has been update successfully.", "status_code": 201
        }
        return JsonResponse(response)
