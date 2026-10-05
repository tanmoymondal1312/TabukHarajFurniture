"""Template tags for the two site languages (Arabic / English).

    {% load site_lang %}
    {% t "Plain text" %}                 -> translated, escaped
    {% th "Text with <b>html</b>" %}     -> translated, not escaped
    {% tf "%(n)s items" n=count %}       -> translated with printf style values
    {% current_language as lang %}       -> "ar" or "en"
    {% current_direction %}              -> "rtl" or "ltr"
    {{ title|bidi_fix }}                 -> keeps 3x4 / 9:00-22:00 readable in RTL
"""

import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from pages.translations import AVAILABLE_LANGUAGES, TRANSLATIONS

register = template.Library()

# A number group, optionally followed by more groups split by a separator
# (dash, slash, colon-less x) or spaces:  180x200, 9:00-22:00, 058 232 8389
_NUM_GROUP = re.compile(
    r"\d[\d.,:]*+(?:\s*[–—\-−/×]\s*\d[\d.,:]*+|\s+\d[\d.,:]*+)+"
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
    """Wrap number groups (3x4, 9:00-22:00, 058 232 8389) in an LTR isolate.

    Without this, RTL text renders them reversed: 4x3, 22:00-9:00.
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
