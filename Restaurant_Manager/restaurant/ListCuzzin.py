from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from marshmallow import ValidationError

from account import Exceptions
from account.schema import UpdateAccountSchema
from restaurant.models import Cuzzin
from restaurant.schema import UpdateDeleteSchema

@require_http_methods(["GET"])
@csrf_exempt
@Exceptions.api_exception_handler
def ListCuzzins(request):
    response = dict()
    cuzzins = list()
    response["data"]=list()
    schema=UpdateAccountSchema()
    data,error=schema.load(request.GET)
    if error:
        raise Exceptions.BadRequestData(errors=error)
    user = data["user"]
    cuzzins = Cuzzin.objects.filter(CuzzinID__id = user.id)

    for cuzzin in cuzzins:
        response["data"].append(
            {
                "cuzzin_id":cuzzin.id,
                "categories":cuzzin.categories,
                "favorites":cuzzin.favorites,
                "dishes":cuzzin.dishes
            }
        )

    response["messages"]="Cuzzin data for given user account"
    response["status_code"]=200
    return JsonResponse(response)