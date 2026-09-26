import secrets
from urllib.parse import urlparse

from django.utils import timezone
from django.utils import translation

from .models import VisitorLog


class DashboardLanguageMiddleware:
    """Dashboard UI is English; the public site stays Arabic."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/dashboard/"):
            return self.get_response(request)
        previous = translation.get_language()
        translation.activate("en")
        try:
            return self.get_response(request)
        finally:
            translation.activate(previous)

SKIP_PREFIXES = (
    "/dashboard/",
    "/admin/",
    "/static/",
    "/media/",
    "/sitemap.xml",
    "/robots.txt",
)
BOT_MARKERS = (
    "bot",
    "crawl",
    "spider",
    "slurp",
    "preview",
    "fetch",
    "monitor",
    "lighthouse",
)
COOKIE_NAME = "th_visitor"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

DESKTOP_UA = ("windows", "macintosh", "x11", "cros", "linux")


def _device(ua):
    ua = (ua or "").lower()
    if "ipad" in ua or "tablet" in ua or ("android" in ua and "mobile" not in ua):
        return VisitorLog.DEVICE_TABLET
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return VisitorLog.DEVICE_MOBILE
    if any(t in ua for t in DESKTOP_UA):
        return VisitorLog.DEVICE_DESKTOP
    return VisitorLog.DEVICE_DESKTOP


def _host(netloc):
    host = netloc.lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return host


class VisitorTrackingMiddleware:
    """Counts public page visits. Stores no IP and no personal data."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self._track(request, response)
        except Exception:
            pass
        return response

    @staticmethod
    def _track(request, response):
        if request.method != "GET":
            return
        if response.status_code not in (200, 304):
            return
        if request.path.startswith(SKIP_PREFIXES):
            return
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return
        ua = request.META.get("HTTP_USER_AGENT") or ""
        low = ua.lower()
        if any(marker in low for marker in BOT_MARKERS):
            return
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            return

        visitor_key = request.COOKIES.get(COOKIE_NAME)
        if not visitor_key:
            visitor_key = secrets.token_urlsafe(12)
            response.set_cookie(
                COOKIE_NAME,
                visitor_key,
                max_age=COOKIE_MAX_AGE,
                path="/",
                samesite="Lax",
                secure=request.is_secure(),
            )

        referrer = request.META.get("HTTP_REFERER") or ""
        ref_host = urlparse(referrer).netloc
        site_host = urlparse(request.build_absolute_uri("/")).netloc
        if not referrer:
            referrer = "Direct"
        elif _host(ref_host) == _host(site_host):
            referrer = "On site"
        else:
            referrer = _host(ref_host)[:200]

        VisitorLog.objects.create(
            path=request.get_full_path()[:300],
            visitor_key=visitor_key[:40],
            referrer=referrer,
            device=_device(ua),
            created_at=timezone.now(),
        )
