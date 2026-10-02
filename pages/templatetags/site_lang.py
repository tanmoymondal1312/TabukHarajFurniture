"""Template tags for the two site languages (Arabic / English).

    {% load site_lang %}
    {% t "Plain text" %}                 -> translated, escaped
    {% th "Text with <b>html</b>" %}     -> translated, not escaped
    {% tf "%(n)s items" n=count %}       -> translated with printf style values
    {% current_language as lang %}       -> "ar" or "en"
    {% current_direction %}              -> "rtl" or "ltr"
"""

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from pages.translations import AVAILABLE_LANGUAGES, TRANSLATIONS

register = template.Library()


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


@register.simple_tag
def current_language():
    return current_lang()


@register.simple_tag
def current_direction():
    return "rtl" if current_lang() == "ar" else "ltr"
