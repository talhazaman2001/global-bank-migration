from fastapi import Request
from prometheus_client import Counter, Histogram
from typing import Callable

class MetricsMiddleware:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.request_count = Counter(
            'http_requests_total', 
            'Total HTTP requests', 
            ['service', 'method', 'endpoint', 'status']
        )
        self.request_latency = Histogram(
            'http_request_duration_seconds', 
            'HTTP request latency',
            ['service']
        )

    async def __call__(self, request: Request, call_next: Callable):
        import time
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        self.request_count.labels(
            service=self.app_name,
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        self.request_latency.labels(
            service=self.app_name
        ).observe(duration)
        
        return response