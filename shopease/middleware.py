from django.http import HttpResponse


class AdminHostMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        # Static files and favicon
        if path.startswith("/static/") or path == "/favicon.ico":
            return self.get_response(request)

        # Admin pages are allowed
        # Django admin login will handle authentication.
        if path.startswith("/admin/"):
            return self.get_response(request)

        # Customer website is allowed on localhost and Render
        return self.get_response(request)