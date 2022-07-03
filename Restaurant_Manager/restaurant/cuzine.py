from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from account import Exceptions
from account.http_tools import make_response
from account.models import Users
from restaurant.models import Cuzzin
from restaurant.schema import CreateCuzzinSchema, GetCuzzinSchema, UpdateDeleteSchema
from restaurant.views import CuisineListCreateView




class CreateCuisine(CuisineListCreateView):
    schema_class = CreateCuzzinSchema
    model = Cuzzin

    def post(self, request, *args, **kwargs):
        user_id = self.req_data.pop("user_id")
        user = Users.objects.get(id = user_id)
        response = dict()
        if not user:
            raise ValueError("user doesn't exist in the system")
        try:
            cuzzin = self.model.objects.create(**self.req_data, CuzzinID_id=user.id)
        except ValueError as e:
            raise Exceptions.BadRequestData(errors=str(e))
        response["categories"] = cuzzin.categories
        response["username"] = str(cuzzin.CuzzinID)
        response["cuzzin_id"] = str(cuzzin.id)
        response["messages"] = "cuzzin is successfully created"
        response["status_code"] = 201
        return JsonResponse(make_response(response), status=201)





@require_http_methods(["GET"])
@csrf_exempt
@Exceptions.api_exception_handler
def GetCuzzin(request):
    schema=GetCuzzinSchema()
    response=dict()
    data,error=schema.load(request.GET)
    if error:
        raise Exceptions.BadRequestData(errors=error)
    cuzzin = data["cuzzin"]
    response["cuzzin_details"]={
        "categories":cuzzin.categories,
        "favorites":cuzzin.favorites,
        "dishes":cuzzin.dishes,
        "cuzzin_id":cuzzin.id,
        "status_code":202
    }
    return JsonResponse(response)

@require_http_methods(["PUT"])
@csrf_exempt
@Exceptions.api_exception_handler
def UpdateCuzzin(request):
    schema=UpdateDeleteSchema()
    response = dict()
    data,error = schema.loads(request.body)
    if error:
        raise Exceptions.BadRequestData(errors=error)
    cuzzin = data["cuzzin"]
    cuzzin.update_fields(cuzzin,**data)
    response["messages"]="Cuzzin information successfully updated"
    return JsonResponse(response)

@require_http_methods(["DELETE"])
@csrf_exempt
@Exceptions.api_exception_handler
def DeleteCuzzin(request):
    schema=UpdateDeleteSchema()
    response=dict()
    data,error = schema.loads(request.body)
    if error:
        raise Exceptions.BadRequestData(errors=error)
    cuzzin = data["cuzzin"]
    cuzzin.delete_obj(cuzzin)
    response["messages"]="cuzzin information deleted successfully"
    response["status_code"]=201
    return JsonResponse(response)

