"""Public site language switch.

Default language is always Arabic. A visitor can switch with a link
such as /products/?lang=en — the choice is saved in a browser cookie
and the whole page renders in that language.

The address bar stays clean and never grows:
- ?lang=en is kept while English is active (and only once, even if an
  old link stacked several lang values),
- ?lang=ar (the default) and unknown codes are removed with a redirect,
  so switching back to Arabic makes the language part vanish.

The dashboard is not affected: DashboardLanguageMiddleware keeps the
dashboard in English.
"""

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation

COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # one year


class LanguageSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")
        self.available = tuple(code for code, _ in settings.LANGUAGES)
        self.default = settings.LANGUAGE_CODE

    def _set_cookie(self, response, request, value):
        response.set_cookie(
            self.cookie_name,
            value,
            max_age=COOKIE_MAX_AGE,
            path="/",
            samesite="Lax",
            secure=request.is_secure(),
        )

    def __call__(self, request):
        param = request.GET.get("lang")
        valid = param in self.available

        # English always lives at ?lang=en. If a visitor with the English
        # cookie lands on a clean URL, redirect once so the address bar,
        # canonical tag and hreflang all show the same stable URL.
        if (
            request.method == "GET"
            and "lang" not in request.GET
            and not request.path.startswith("/admin/")
            and not request.path.startswith("/dashboard/")
        ):
            cookie_lang = request.COOKIES.get(self.cookie_name, "")
            if cookie_lang in self.available and cookie_lang != self.default:
                params = request.GET.copy()
                params["lang"] = cookie_lang
                redirect = HttpResponseRedirect(
                    request.path + "?" + params.urlencode()
                )
                self._set_cookie(redirect, request, cookie_lang)
                return redirect

        # Rebuild the query string with at most one lang value. Arabic
        # (the default) and unknown codes are dropped, English stays.
        # If the URL was dirty (grown or default lang), redirect once.
        if request.method == "GET" and "lang" in request.GET:
            params = request.GET.copy()
            params.pop("lang", None)
            keep = param if (valid and param != self.default) else None
            if keep:
                params["lang"] = keep
            clean_qs = params.urlencode()
            if clean_qs != request.META.get("QUERY_STRING", ""):
                redirect = HttpResponseRedirect(
                    request.path + ("?" + clean_qs if clean_qs else "")
                )
                if valid:
                    self._set_cookie(redirect, request, param)
                return redirect

        if valid:
            chosen = param
        else:
            chosen = request.COOKIES.get(self.cookie_name, "")
            if chosen not in self.available:
                chosen = self.default

        translation.activate(chosen)
        try:
            response = self.get_response(request)
        finally:
            translation.deactivate()

        if valid:
            self._set_cookie(response, request, chosen)
        return response
