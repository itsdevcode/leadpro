from starlette.types import ASGIApp, Receive, Scope, Send
from redis.asyncio import Redis
from starlette.responses import JSONResponse

class RateLimitMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        redis_client: Redis,
        limit: int = 5,
        window_seconds: int = 60,
    ):
        self.app = app
        self.redis = redis_client
        self.limit = limit
        self.window_seconds = window_seconds
        self.protected_routes = {
            ("POST", "/api/v1/users/login"),
            ("POST", "/api/v1/users/otp/verify"),
        }

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        client = scope["client"]
        method = scope["method"]
        path = scope["path"]
        
        if (method, path) not in self.protected_routes:
            await self.app(scope, receive, send)
            return

        
        ip_address = client[0]

        key = f"rate_limit:{ip_address}:{method}:{path}"

        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, self.window_seconds)
        
        
        if count > self.limit:
            ttl = await self.redis.ttl(key)

            response = JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
                headers={"Retry-After": str(max(ttl, 0))},
            )

            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)