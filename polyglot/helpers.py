from django.utils import translation
from polyglot import defaults

def format_field_name(normalized_field_name,
                      field_format=defaults.FIELD_FORMAT,
                      language=None):
    if not language:
        language = translation.get_language()[:2]
    if field_format == 'prefix':
        field_name = "%s_%s" % (language, normalized_field_name)
    elif field_format == 'suffix':
        field_name = "%s_%s" % (normalized_field_name, language)
    return field_name

def normalize_field_name(normalized_field_name,
                         field_format=defaults.FIELD_FORMAT):
    if field_format == 'prefix':
        normalized_field_name = field_name[3:]
    elif field_format == 'suffix':
        normalized_field_name = field_name[:-3]
    return normalized_field_name
