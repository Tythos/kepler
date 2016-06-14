"""Defines unit tests for the satcat service and supporting behvaiors.
"""

import unittest
import urlparse
from kepler import satcat, data

class EntryTests(unittest.TestCase):
    def test_import(self):
        satCatPath = data.get_path('satcat.txt')
        with open(satCatPath, 'r') as f:
            sc = satcat.Entry.fromFile(f)
        self.assertTrue(len(sc) > 0)
        
class ServiceTests(unittest.TestCase):
    def test_parse(self):
        svc = satcat.Service()
        url = 'http://test.com/tle/25544'
        urlObj = urlparse.urlparse(url)
        tle = svc.tle(urlObj, None)
        self.assertTrue(tle.startswith('ISS'))

if __name__ == '__main__':
    unittest.main()
        