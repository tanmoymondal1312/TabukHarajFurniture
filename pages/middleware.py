"""Public site language switch.

Default language is always Arabic. A visitor can switch with a link
such as /products/?lang=en — the choice is saved in a browser cookie
and the whole page renders in that language.

The dashboard is not affected: DashboardLanguageMiddleware keeps the
dashboard in English.
"""

from django.conf import settings
from django.utils import translation

COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # one year


class LanguageSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")
        self.available = tuple(code for code, _ in settings.LANGUAGES)
        self.default = settings.LANGUAGE_CODE

    def __call__(self, request):
        chosen = None

        param = request.GET.get("lang")
        if param in self.available:
            chosen = param

        if chosen is None:
            chosen = request.COOKIES.get(self.cookie_name, "")
            if chosen not in self.available:
                chosen = self.default

        translation.activate(chosen)
        try:
            response = self.get_response(request)
        finally:
            translation.deactivate()

        if param in self.available:
            response.set_cookie(
                self.cookie_name,
                chosen,
                max_age=COOKIE_MAX_AGE,
                path="/",
                samesite="Lax",
                secure=request.is_secure(),
            )
        return response
