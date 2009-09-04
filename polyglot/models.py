# -*- coding: utf-8 -*-
import sys

# Just create models when testing
if sys.argv[1] == 'test':

    from django.db import models
    from polyglot.decorators import *
    from polyglot.managers import *
    from django.conf import settings

    settings.LANGUAGE_CODE = 'en'

    settings.LANGUAGES = (
        ('en', u'English'),
        ('es', u'Español'),
    )

    @normalize_fields_pre
    class TestPre(models.Model):
        en_test = models.CharField(max_length=32)
        es_test = models.CharField(max_length=32)

    @normalize_fields_post
    class TestPost(models.Model):
        test_en = models.CharField(max_length=32)
        test_es = models.CharField(max_length=32)

    class TestManager(models.Model):
        test = models.CharField(max_length=32)
        language = models.CharField(max_length=2, choices=settings.LANGUAGES)
        objects = LanguageManager()

        def __unicode__(self):
            return self.test
