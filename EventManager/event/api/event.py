from django.http import JsonResponse
from django.views import View
from EventManager.event.api.schema import UserSchema, EventSchema, EventRatingSchema
from EventManager.event.exceptions import BadRequestData
from EventManager.event.models import Users, EventInfo


class RegisterUser(View):
    schema = UserSchema()
    model = Users

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterUser, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data, errors = self.schema.loads(request.body)
        if errors:
            raise BadRequestData(errors=errors)

        email = data.pop("email") if "email" in data else None
        password = data.pop("password")
        username = data.pop("username")
        self.model.objects.create_user(username=username, email=email, password=password, **data)
        response = dict()
        response["payload"] = {
            "message": "User has been registered successfully.", "status_code": 201
        }
        return JsonResponse(response)


class RegisterEvent(View):
    schema = EventSchema()
    model = EventInfo

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterEvent, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data, errors = self.schema.loads(request.body)
        if errors:
            raise BadRequestData(errors=errors)
        self.model.objects.create(**data)
        response = dict()
        response["payload"] = {
            "message": "User has been registered successfully.", "status_code": 201
        }
        return JsonResponse(response)


class UpdateEventRating(View):
    schema = EventRatingSchema()
    model = EventInfo

    def dispatch(self, request, *args, **kwargs):
        return super(UpdateEventRating, self).dispatch(request, *args, **kwargs)

    def put(self, request, id, *args, **kwargs):
        data, errors = self.schema.loads(request.body)
        if errors:
            raise BadRequestData(errors=errors)

        rating = data.get("rating")

        self.model.objects.filter(id=data.get("event_id")).update(rating=rating)


class UserEventMapping(View):
    schema = UserSchema()
    model = Users

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterUser, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data, errors = self.schema.loads(request.body)
        if errors:
            raise BadRequestData(errors=errors)
        pass
