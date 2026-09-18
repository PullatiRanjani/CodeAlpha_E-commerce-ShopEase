from django.http import HttpResponse


class AdminHostMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        host = request.get_host().split(":")[0]
        path = request.path

        # Allow static files and favicon on both local hosts
        if path.startswith("/static/") or path == "/favicon.ico":
            return self.get_response(request)

        # Admin pages only through localhost
        if path.startswith("/admin/"):

            if host != "localhost":
                return HttpResponse(
                    "Admin access is available only through localhost.",
                    status=403
                )

        # Customer website only through 127.0.0.1
        else:

            if host != "127.0.0.1":
                return HttpResponse(
                    "Customer website is available only through 127.0.0.1.",
                    status=403
                )

        return self.get_response(request)