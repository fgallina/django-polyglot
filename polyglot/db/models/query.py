from django.db.models import Q
from django.db.models.sql.constants import QUERY_TERMS
from polyglot.helpers import format_field_name

def QT(field_lookup, value):
    lookup_pos = -1
    for lookup in QUERY_TERMS.keys():
        ltemp = field_lookup.rfind(lookup)
        if ltemp != -1:
            lookup_pos = ltemp
            break
    # we have a lookup
    if lookup_pos != -1:
        field_ = field_lookup[:lookup_pos-3]
        lookup = field_lookup[lookup_pos-3:]
    else:
        field_ = field_lookup
        lookup = ''
    field_pos = field_.rfind('__')
    # we don't have a relationship
    if field_pos == -1:
        field = field_
    else:
        field = field_[field_.rfind('__')+2:]
    relationship = field_[:field_.rfind(field)]
    field = format_field_name(field)
    q = relationship + field + lookup
    kwargs = {str(q): value}
    return Q(**kwargs)

def T(normalized_field_name):
    return format_field_name(normalized_field_name)
