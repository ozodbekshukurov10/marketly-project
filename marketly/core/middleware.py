import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseForbidden


SECURITY_FILE = Path(settings.BASE_DIR) / 'data' / 'security.json'
SUSPICIOUS_PATTERNS = (
    '.env',
    'wp-admin',
    'phpmyadmin',
    '../',
    '<script',
    'union select',
)


def _read_security_config():
    if not SECURITY_FILE.exists():
        return {'enabled': True}

    try:
        data = json.loads(SECURITY_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'enabled': True}

    return {'enabled': bool(data.get('enabled', True))}


class MarketlySecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        security_config = _read_security_config()
        request.marketly_security_enabled = security_config['enabled']

        if security_config['enabled']:
            path_and_query = f'{request.path} {request.META.get("QUERY_STRING", "")}'.lower()
            if any(pattern in path_and_query for pattern in SUSPICIOUS_PATTERNS):
                return HttpResponseForbidden("So'rov xavfsizlik sabab bloklandi")

        response = self.get_response(request)

        if security_config['enabled']:
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['Referrer-Policy'] = 'same-origin'
            response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
            if request.is_secure():
                response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "img-src 'self' https: data:; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com https://fonts.googleapis.com data:; "
                "script-src 'self' 'unsafe-inline'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )

        if request.path.endswith('admin-panel.html') or request.path.endswith('admin-security.html'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'

        return response
