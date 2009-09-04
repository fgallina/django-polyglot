from django import http
from django.conf import settings
from django.utils import translation

def set_language_replace(request, cut_next=False):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    if request.method == 'POST':
        lang_code = request.POST.get('language', settings.LANGUAGES[0][0])
        old_lang = translation.get_language()[:2];
        next = next.replace('/' + old_lang + '/', '/' + lang_code + '/', 1)
        if cut_next:
            next = next[:next.find(lang_code)] + lang_code + '/'
        response = http.HttpResponseRedirect(next)
        if lang_code and translation.check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    else:
        response = http.HttpResponseRedirect(next)
    return response

def redirect_to_i18n(request, url, **kwargs):
    """
    Redirect to a i18nized given URL.

    The given url may contain dict-style string formatting, which will be
    interpolated against the params in the URL.  For example, to redirect from
    ``/foo/<lang>/`` to ``/bar/<lang>/``, you could use the following URLconf::

        urlpatterns = patterns('',
            ('^foo/$', 'fromthecloud.globaltags.views.redirect_to_i18n', {'url' : '/bar/'}),
        )

    If the given url is ``None``, a HttpResponseGone (410) will be issued.
    """
    url = url + translation.get_language()[:2] + '/'
    if url is not None:
        return http.HttpResponsePermanentRedirect(url % kwargs)
    else:
        return http.HttpResponseGone()
