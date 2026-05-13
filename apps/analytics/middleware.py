"""
Smart Tourism — Visitor Tracking Middleware
Logs every API request as a VisitorActivity row (async via Celery).
Only tracks GET requests to /api/v1/places/ and a few key write endpoints.
"""
import threading

_local = threading.local()

# Paths we want to track (prefix match)
TRACKED_PATHS = [
    '/api/v1/places/',
    '/api/v1/bookings/',
    '/api/v1/cabs/bookings/',
    '/api/v1/reviews/',
    '/api/v1/travel-plans/',
]

# Heavy write actions that map cleanly to activity types
METHOD_ACTION_MAP = {
    'POST': {
        '/api/v1/bookings/':       'create_booking',
        '/api/v1/cabs/bookings/':  'book_cab',
        '/api/v1/reviews/':        'write_review',
        '/api/v1/travel-plans/':   'create_plan',
        '/api/v1/auth/login/':     'login',
        '/api/v1/auth/register/':  'register',
    }
}


class VisitorTrackingMiddleware:
    """Lightweight middleware — defers DB writes to Celery."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only track successful API calls
        if response.status_code < 400 and request.path.startswith('/api/v1/'):
            try:
                self._track(request, response)
            except Exception:
                pass   # Never break the request cycle

        return response

    def _track(self, request, response):
        from apps.analytics.tasks import log_visitor_activity

        path   = request.path
        method = request.method
        user_id = request.user.id if request.user.is_authenticated else None

        # Determine action
        action = None
        if method == 'GET' and any(path.startswith(p) for p in TRACKED_PATHS):
            action = 'view_place' if '/places/' in path else 'view_page'
        elif method in METHOD_ACTION_MAP:
            for prefix, act in METHOD_ACTION_MAP[method].items():
                if path.startswith(prefix):
                    action = act
                    break

        if not action:
            return

        # Fire-and-forget Celery task
        log_visitor_activity.delay(
            user_id=user_id,
            action=action,
            ip_address=self._get_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            path=path,
        )

    @staticmethod
    def _get_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')