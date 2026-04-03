"""
Custom middleware for EdgeTravel security.
"""
import time
from collections import defaultdict
from django.http import HttpResponseForbidden
from django.conf import settings


class RateLimitMiddleware:
    """
    Rate limits login attempts by IP address to prevent brute force attacks.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_attempts = defaultdict(list)

    def __call__(self, request):
        if request.path == settings.LOGIN_URL and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            window = settings.RATE_LIMIT_LOGIN_WINDOW
            max_attempts = settings.RATE_LIMIT_LOGIN_ATTEMPTS

            # Clean old attempts
            self.login_attempts[ip] = [
                t for t in self.login_attempts[ip] if now - t < window
            ]

            if len(self.login_attempts[ip]) >= max_attempts:
                return HttpResponseForbidden(
                    '<h1>Too Many Login Attempts</h1>'
                    '<p>Please wait a few minutes before trying again.</p>'
                )

            self.login_attempts[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
