#! -*- coding: utf-8 -*-
from django.db import models
import unittest
from django.conf import settings
from polyglot.models import *

class ManagersTestCase(unittest.TestCase):

    def setUp(self):
        self.test_en = TestManager.objects.create(test='english', language='en')
        self.test_es = TestManager.objects.create(test='español', language='es')

    def testManager(self):
        if settings.LANGUAGE_CODE[:2] == 'en':
            self.assertEquals(TestManager.objects.lall()[0], self.test_en)
        elif settings.LANGUAGE_CODE[:2] == 'es':
            self.assertEquals(TestManager.objects.lall()[0], self.test_es)
