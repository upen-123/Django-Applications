from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from account import Exceptions
import json
from account.decorator import api_token_required

class CuisineView(View):
    schema_class = None
    def __init__(self,*args, **kwargs):
        super(CuisineView,self).__init__(*args,**kwargs)

    def make_response(self,data):
        if isinstance(data,dict):
            return {"response":data, "meta":{}}
        else:
            raise Exceptions.BadRequestData()

class CuisineListCreateView(CuisineView):
    http_method_names = ["get","post"]


    @method_decorator(Exceptions.api_exception_handler)
    @method_decorator(api_token_required)
    def dispatch(self,request, *args,**kwargs):

        self.schema = self.schema_class()
        errors = None

        if request.method == 'GET':
            self.req_params ,errors = self.schema.load(request.GET)

        # check schema for POST request
        elif request.method == "POST":
            if not request.body:
                raise Exceptions.BadRequestData()

            elif isinstance(json.loads(request.body), list):
                self.schema = self.schema_class(many=True)
            else:
                pass
            self.req_data, errors = self.schema.loads(request.body)

        else:
            raise Exceptions.MethodNotAllowed(request.method)

        # schema errors to be captured here
        if errors:
            raise Exceptions.BadRequestData(errors=errors)

        return super(CuisineView,self).dispatch(request,*args,**kwargs)


    def get(self, request, *args, **kwargs):
        raise Exceptions.NotImplemented()

    def post(self, request, *args, **kwargs):
        raise Exceptions.NotImplemented()
