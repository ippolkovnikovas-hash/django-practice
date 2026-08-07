import time
from django.http import HttpRequest, HttpResponse, JsonResponse


def setup_useragent_on_request_middleware(get_response):

    print("initial call")

    def middleware(request: HttpRequest, *args, **kwargs):
        print("before get response")
        request.user_agent = request.META.get("HTTP_USER_AGENT")
        response = get_response(request)
        print("after get response")
        return response

    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest, *args, **kwargs):
        self.request_count += 1
        print("request count", self.request_count)
        response = self.get_response(request)
        self.response_count += 1
        print("response count", self.response_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exceptions so far")


class ThrottlingMiddleware:
    RATE_LIMIT_SECONDS = 2

    def __init__(self, get_response):
        self.get_response = get_response
        self.last_request_time: dict[str, float] = {}

    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        ip = request.META.get("REMOTE_ADDR", "unknown")
        now = time.time()

        last_time = self.last_request_time.get(ip)
        if last_time is not None and now - last_time < self.RATE_LIMIT_SECONDS:
            return JsonResponse({"error": "Слишком много запросов"}, status=429)

        self.last_request_time[ip] = now
        return self.get_response(request)