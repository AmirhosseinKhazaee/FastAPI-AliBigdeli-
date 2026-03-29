from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Process the request and get the response from the next handler
        response = await call_next(request)

        # 2. Modify the response (add your custom header)
        response.headers["test"] = "hello"

        # 3. Return the modified response
        return response
