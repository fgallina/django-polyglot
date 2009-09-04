#! -*- coding: utf-8 -*-
from django.db import models
import unittest
from django.conf import settings
from polyglot.models import *

class DecoratorsTestCase(unittest.TestCase):

    def setUp(self):
        self.test_pre = TestPre.objects.create(en_test='english', es_test='spanish')
        self.test_post = TestPost.objects.create(test_en='english', test_es='spanish')

    def testPre(self):
        if settings.LANGUAGE_CODE[:2] == 'en':
            self.assertEquals(self.test_pre.en_test, self.test_pre.test)
        elif settings.LANGUAGE_CODE[:2] == 'es':
            self.assertEquals(self.test_pre.es_test, self.test_pre.test)

    def testPost(self):
        if settings.LANGUAGE_CODE[:2] == 'en':
            self.assertEquals(self.test_post.test_en, self.test_post.test)
        elif settings.LANGUAGE_CODE[:2] == 'es':
            self.assertEquals(self.test_post.test_es, self.test_post.test)
