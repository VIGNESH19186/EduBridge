from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ForceEnglishMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ensure Accept-Language header is set to English for downstream handlers
        try:
            headers = dict(request.headers)
            headers["accept-language"] = "en"
            # Replace scope headers with updated values (bytes pairs)
            request.scope["headers"] = [
                (k.encode("latin-1"), v.encode("latin-1")) for k, v in headers.items()
            ]
        except Exception:
            # If anything goes wrong, continue without failing the request
            pass

        response = await call_next(request)
        return response
