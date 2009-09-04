from django import template
from django.utils import translation
from django.conf import settings
from ..polyglot import defaults
from ..polyglot.helpers import format_field_name
register = template.Library()

def polyglot_trans(parser, token):
    """
    {% polyglot_trans object field [lang=<lang>[,format=pre|post]] %}
    """
    args = token.split_contents()
    args.reverse()
    tag = args.pop()
    args.reverse()

    if len(args) < 2:
        raise TemplateSyntaxError(
            "'%s' tag received a bad argument: "
            "'%s'" % (tag, args))

    try:
        str_options = args[2]
    except IndexError:
        str_options = None

    optionskwargs = {}

    if str_options:
        options = str_options.split(',')
        for option in options:
            pair = option.split('=')
            optionskwargs[str(pair[0])] = pair[1]

    return PolyglotTransNode(args[0], args[1], **optionskwargs)


class PolyglotTransNode(template.Node):

    def __init__(self, obj, field, lang=u'', format=defaults.FIELD_FORMAT):
        self.object = obj
        self.field = field
        if not lang:
            self.lang = translation.get_language()[:2]
        else:
            self.lang = lang
        self.format = format

    def render(self, context):
        print self.field
        try:
            tfield = format_field_name(self.field, language=self.lang)
            return getattr(context[self.object], tfield)
        except:
            return ''

register.tag('polyglot_trans', polyglot_trans)
