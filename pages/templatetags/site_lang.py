"""Template tags for the two site languages (Arabic / English).

    {% load site_lang %}
    {% t "Plain text" %}                 -> translated, escaped
    {% th "Text with <b>html</b>" %}     -> translated, not escaped
    {% tf "%(n)s items" n=count %}       -> translated with printf style values
    {% current_language as lang %}       -> "ar" or "en"
    {% current_direction %}              -> "rtl" or "ltr"
    {{ title|bidi_fix }}                 -> keeps phone numbers like 058 232 8389 readable in RTL
"""

import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from pages.translations import AVAILABLE_LANGUAGES, TRANSLATIONS

register = template.Library()

# Phone-style numbers: digit groups split only by spaces (058 232 8389).
# Ranges joined by punctuation (3x4, 9:00-22:00) are NOT matched:
# Arabic readers read ranges right-to-left, which is the default
# bidi behaviour, so they must stay un-isolated (W3C i18n advice).
_NUM_GROUP = re.compile(
    r"\+?[0-9][0-9.,:]*+(?:\s+[0-9][0-9.,:]*+)+"
)


def current_lang():
    lang = (get_language() or "ar").replace("_", "-").split("-")[0].lower()
    return lang if lang in AVAILABLE_LANGUAGES else "ar"


def translate(msgid):
    lang = current_lang()
    if lang == "en":
        return msgid
    return TRANSLATIONS.get(lang, {}).get(msgid, msgid)


@register.simple_tag
def t(msgid):
    return translate(msgid)


@register.simple_tag
def th(msgid):
    return mark_safe(translate(msgid))


@register.simple_tag
def tf(msgid, **kwargs):
    text = translate(msgid)
    try:
        return text % kwargs
    except Exception:
        return text


@register.filter
def bidi_fix(value):
    """Wrap phone-style numbers (058 232 8389) in an LTR isolate.

    Phone numbers must read left-to-right, so the groups are isolated.
    Ranges (3x4, 9:00-22:00) are left alone: Arabic readers read them
    right-to-left, which is what the bidi algorithm already does.
    """
    if value is None:
        return ""
    text = escape(str(value))
    return mark_safe(
        _NUM_GROUP.sub(lambda m: '<bdi dir="ltr">%s</bdi>' % m.group(0), text)
    )


@register.simple_tag(takes_context=True)
def lang_url(context, target):
    """Link to the same page in another language without stacking params.

    Keeps the other query params (cat, q, ...) and replaces any old
    lang value with the target one, so ?lang= never grows. Arabic is
    the default language, so the middleware strips its param again.
    """
    request = context.get("request")
    if request is None:
        return "?lang=%s" % target
    params = request.GET.copy()
    params["lang"] = str(target)
    return "?%s" % params.urlencode()


@register.simple_tag
def current_language():
    return current_lang()


@register.simple_tag
def current_direction():
    return "rtl" if current_lang() == "ar" else "ltr"
