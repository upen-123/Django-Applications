from functools import wraps
from django.http import JsonResponse
from django.utils.encoding import force_text


def api_exception_handler(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except APIException as e:
            return JsonResponse({"message": str(e.detail), "error": e.errors, "status_code": e.code}, status=e.code)

    return decorated_function


class APIException(Exception):
    status_code = 500
    default_detail = "A server error occurred."

    def __init__(self, detail=None, errors=None, code=None):

        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail

        self.errors = errors

        if code is None:
            self.code = self.status_code
        else:
            self.code = code

    def __str__(self):
        return self.detail


class BadRequestData(APIException):
    status_code = 400
    default_detail = "Bad request data."


class MethodNotAllowed(APIException):
    status_code = 405
    default_detail = 'Method "{method}" not allowed.'

    def __init__(self, method, detail=None):
        if detail is not None:
            self.detail = force_text(detail).format(method=method)
        else:
            self.detail = force_text(self.default_detail).format(method=method)
        super(MethodNotAllowed, self).__init__()
