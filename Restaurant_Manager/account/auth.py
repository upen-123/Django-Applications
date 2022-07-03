from django.utils import timezone
import jwt
from account.decorator import  api_token_required
from account.decorator import  generate_random_alphenumeric_number
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from account import Exceptions, decorator
from account.http_tools import make_response
from account.models import Users
from account.schema import RegisterAccountSchema, GetUserProfileSchema, LogInSchema, UpdateAccountSchema
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings

User = get_user_model()

@require_http_methods(["POST"])
@csrf_exempt
@Exceptions.api_exception_handler
def RegisterAccount(request):
    """
    for Creating account of user
    :param request:
    ###########
    second commit
    :return:
    """
    schema = RegisterAccountSchema()
    response = dict()
    data,error = schema.loads(request.body)
    if error:
        raise Exceptions.BadRequestData(errors=error)
#    import pdb;pdb.set_trace()
    username = data.pop("username")
    password = data.pop("password")
    try:
        user = User.objects.create_user(username=username,email=None,password=password,**data)
    except ValueError as e:
        raise Exceptions.BadRequestData(errors=str(e))
    response['messages']="User's account is successful created"
    response['username']=user.username
    response['user_id']=str(user.id)
    response['status_code']=201

    return JsonResponse(response)


@require_http_methods(["POST"])
@decorator.set_request_session
@csrf_exempt
@Exceptions.api_exception_handler
def login(request):
    schema = LogInSchema()
    response = dict()
    data, error = schema.loads(request.body)
    if error:
        raise Exceptions.BadRequestData(errors=error)
    user = authenticate(username=data["username"],password=data["password"])
    if not user:
        raise Exceptions.BadRequestData(errors="Either Invalid credentials or Account is not active.")

    session_id = generate_random_alphenumeric_number(32)
    session = request.session_table
    exp_time = request.session_exp_time
    try:
        user_session = session.objects.get(user=user)
        user_session.delete()
    except session.DoesNotExist:
        pass
    session.objects.create(user=user,session_id = session_id)
    JWT_private_key = "/home/upendra/Documents/jwt-key-sample_project"

    private_key = open(JWT_private_key).read()
    payload = {
        "user_id": str(user.id),
        "exp": (timezone.now() + timezone.timedelta(hours=5)),
        "session_id":session_id,
    }
    token = jwt.encode(payload,private_key,algorithm = "RS256").decode("utf-8")

    response["token"] = token
    response["username"] = data["username"]
    response["user_id"] = str(user.id)
    response["messages"] = "you are logged in"
    return JsonResponse(make_response(response),status = 201)

@require_http_methods(["POST"])
@csrf_exempt
@Exceptions.api_exception_handler
@api_token_required
def logout(request):
    response = dict()
    request.session.delete()
    response["messages"] = "logout successfully"
    return JsonResponse(make_response(response))


@require_http_methods(["GET"])
@csrf_exempt
@api_token_required
@Exceptions.api_exception_handler
def getUserProfile(request):
    schema = GetUserProfileSchema()
    response = dict()
    data,error = schema.load(request.GET)
    if error:
        raise Exceptions.BadRequestData(errors=error)
#    import pdb;pdb.set_trace()
    user = data["user"]

    response["profile_details"]={
        "username":user.username,
        "first_name":user.first_name,
        "last_name":user.last_name,
    }
    return JsonResponse(response)


@require_http_methods(["PUT"])
@csrf_exempt
@api_token_required
@Exceptions.api_exception_handler
def UpdateUserInfo(request):
    response = dict()
    schema = UpdateAccountSchema()
#    import pdb;pdb.set_trace()
    data,error = schema.loads(request.body)
    if error:
        raise Exceptions.BadRequestData(errors=error)
    user = data["user"]
    user.update_fields(user,**data)
    response["message"] = "User Profile Details has been successfully updated."
    response["status_code"] = 202
    return JsonResponse(make_response(response))