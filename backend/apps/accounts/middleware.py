from project import settings

EXCLUDE_FROM_MIDDLEWARE = [
    #  'apps.accounts.views.RegisterAPIView',
    'apps.accounts.views.LoginAPIView',
]


class AuthorizationMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = '.'.join((view_func.__module__, view_func.__name__))
        print(view_name)
        if view_name in EXCLUDE_FROM_MIDDLEWARE:
            return None

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            request.META[
                settings.SIMPLE_JWT["AUTH_HEADER_NAME"]] = f'{settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0]} {token}'
        return self.get_response(request)
