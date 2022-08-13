from .utils import set_current_user


class CurrentUserMiddleware:
    def process_request(self, request):
        set_current_user(getattr(request, 'user', None))
