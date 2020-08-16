"""Test suite for document-converter"""

import sys
import unittest

sys.path.insert(0, 'main/python')  # Execute test from project's root directory

from pdf_to_html_server import app


class TestDocumentConverter(unittest.TestCase):
    """Test suite to test the document converter"""

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_health_check(self):
        """Test for health check method"""
        result = self.app.get('/v1/health')

        # assert the status code of the response 200 (OK)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'UP')

    def test_method_not_supported(self):
        """Test those clients that invoke """
        result = self.app.get('/api/v1.0/documents/convert')
        # assert the status code of the response 405 (method not allowed)
        self.assertEqual(result.status_code, 405)

    def tearDown(self):
        """Tearing down test suite"""


if __name__ == '__main__':
    unittest.main()
