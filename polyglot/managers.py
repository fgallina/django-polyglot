from django.utils import translation
from django.db import models
from django.db.models import Q
from polyglot import defaults
from polyglot import helpers

class LanguageFieldManager(models.Manager):
    """Returns elements of the current language."""

    def lall(self):
        lang = translation.get_language()[:2]
        filterby = {str(defaults.MANAGER_LANG_FIELD): lang}
        return self.get_query_set().filter(**filterby)


class LanguageManager(models.Manager):
    """Returns elements of the current language."""

    def __init__(self, *fields):
        super(LanguageManager, self).__init__()
        self.fields = fields

    def lall(self, *fields):
        if not fields:
            fields = self.fields
        qstring = ''
        for field in fields:
            field_name = helpers.format_field_name(field)
            qstring += 'Q(%s="") | ' % field_name
        qstring = qstring[:-2]
        q = eval(qstring)
        return self.get_query_set().exclude(q)
