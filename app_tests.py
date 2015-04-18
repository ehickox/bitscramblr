# -*- coding: utf-8 -*-
import app
import unittest
from app import controller, forms

class FirstTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.valid_form = forms.RequestForm("1HasACSXrKs42u9ySoSEDRNSCHRSWPpYWT",
                                            "0.4", None)
        self.invalid_form = forms.RequestForm('abc123', '-0.1', None)

    def tearDown(self):
        pass

    def test_form_validation(self):
        self.assertIsNone(self.valid_form.errors.get('destination'))
        self.assertIsNone(self.valid_form.errors.get('amount'))
        
        self.assertIsNotNone(self.invalid_form.errors.get('destination'))
        self.assertIsNotNone(self.invalid_form.errors.get('amount'))

if __name__ == "__main__":
    unittest.main()
