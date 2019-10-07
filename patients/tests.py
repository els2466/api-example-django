# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import CreatePatientIdTable

class IdTableTests(TestCase):

    def test_ids(self):
        # Test that ID and patient names are properly added
        self.assertEqual(CreatePatientIdTable())