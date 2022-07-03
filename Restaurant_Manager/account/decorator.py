import hashlib
import random
import string
import time
from functools import wraps
import json
import jwt
from django.contrib.auth import authenticate, get_user_model
#from django.core.serializers import json
from django.http import JsonResponse
from account import Exceptions
from account.schema import UpdateAccountSchema, LogInSchema



def generate_random_alphenumeric_number(length=6):
    """
    This function would generate a random alphanumeric number using MD5 hash of provided length
    :param length: integer
    :return: random number
    """
    timestamp = int(time.time())
    random_num = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    md5_hash = hashlib.md5((str(timestamp) + random_num).encode("utf-8")).hexdigest()
    return "".join(random.choices(md5_hash, k=length))


def set_request_session(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        body = json.loads(request.body.decode("utf-8"))
        from account.models import UserSession
        request.session_table = UserSession
        request.session_exp_time = 5
        return func(request,*args,**kwargs)
    return inner


def api_token_required(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        request.user = None
        j_token = request.META.get("HTTP_API_TOKEN")
        if j_token:
            try:
                JWT_public_key = "/home/upendra/Documents/jwt-key-sample_project.pub"
                public_key = open(JWT_public_key).read()
                payload = jwt.decode(j_token,public_key,algorithm=["RS256"])
            except (jwt.DecodeError,jwt.ExpiredSignatureError):
                return JsonResponse(
                    {"error":"Token is invalid/expired","message":"Not Authorized request","status_code":"452"},
                    status=401,
                )
            user_model = get_user_model()
            request.user = user_model.objects.get(id=payload["user_id"])
            request.token = j_token

            from account.models import UserSession
            try:
                session = UserSession
                request.session = session.objects.get(user=request.user,session_id = payload["session_id"])
            except session.DoesNotExist:
                return JsonResponse(
                    {"error":"user session doesn't exist","messages":"Not Authorized request","status_code":"453"},
                    status = 401
                )

        else:
            return JsonResponse(
                {"error":"Token is not provided","messages":"Not Authorized request","status_code":"454"},
                status = 401
            )
        return func(request,*args,**kwargs)
    return inner


