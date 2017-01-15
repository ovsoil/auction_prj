from django.test import TestCase
from django.test.client import Client


# Create your tests here.
class AuctionTest(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
