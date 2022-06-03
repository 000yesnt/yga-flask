from flask_testing import TestCase
from yesntga import initialize, db
import unittest 

class MyTest(TestCase):
    def create_app(self):
        return initialize()

    def test_basic(self):
        """Very basic heartbeat. If the app doesn't immediately crash, 
        there's a pretty good chance that it'll run perfectly fine."""
        response = self.client.get('/health')
        self.assert200(response)
        assert 'healthy' in response.json
    
    def test_api_basic(self):
        """same as test_basic but for API routes instead"""
        response = self.client.get('/api/health')
        self.assert200(response)
        assert 'healthy' in response.json
        assert response.json['api_failed'] == False

if __name__ == '__main__':
    unittest.main()