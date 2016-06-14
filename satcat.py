"""Satellite catalog microservice (based on src.service.Service) and supporting
   data exchange models.
"""

import bs4
import re
import requests
from kepler import data
from scrapese import celestrak
from src import service, dxm

@dxm.isdxm
class Entry(object):
    """Satellite catalog entry model, designed around the 128-character catalog
       summary entries documented and used by CelesTrak:
          http://celestrak.com/satcat/satcat-format.asp.
    """
    
    def __init__(self):
        self.launchYear = None
        self.launchNumber = None
        self.launchLoc = None
        self.catNum = None
        self.isMultipleNames = None
        self.isPayload = None
        self.opStatus = None
        self.name = None
        self.source = None
        self.launchDate = None
        self.launchSite = None
        self.decayDate = None
        self.period_min = None
        self.inclination_deg = None
        self.apogee_km = None
        self.perigee_km = None
        self.rcs_m2 = None
        self.orbStatus = None

    @staticmethod
    def fromLine(txt):
        """Constructs and returns an Entry object by parsing the given line of
           text
        """
        obj = Entry()
        for k,v in {
            'launchYear': (0,4),
            'launchNumber': (5,8),
            'launchLoc': (8,11),
            'catNum': (13,18),
            'isMultipleNames': (19,20),
            'isPayload': (20,21),
            'opStatus': (21,22),
            'name': (23,47),
            'source': (49,54),
            'launchDate': (56,66),
            'launchSite': (68,74),
            'decayDate': (75,85),
            'period_min': (87,94),
            'inclination_deg': (96,101),
            'apogee_km': (103,109),
            'perigee_km': (111,116),
            'rcs_m2': (119,127),
            'orbStatus': (129,132)
        }.iteritems():
            setattr(obj, k, txt[v[0]:v[1]])
        return obj
        
    @staticmethod
    def fromFile(hFile):
        """Returns a list of Entry objects derived by reading the given file
           handle, which will be closed regardless of the operation's outcome.
        """
        nTried = 0
        nFailed = 0
        entries = []
        for line in hFile.readlines():
            nTried += 1
            try:
                entries.append(Entry.fromLine(line))
            except:
                nFailed += 1
        hFile.close()
        return entries

class Service(service.Service):
    """Provides a microservice supporting satellite catalog operations,
       primarily basic fetch and refresh.
    """
    
    def __init__(self):
        self.sci = None
        with open(data.get_path('satcat.txt'), 'r') as f:
            self.sci = Entry.fromFile(f)
            
    @service.isop
    def _root(self, url, args):
        """Returns a newline-delimited list of all SSCIDs hosted by this
           satellite catalog.
        """
        res = ''
        for sc in self.sci:
            res += sc.catNum + '\n'
        return res
        
    @service.isop
    def _refresh(self, url, args):
        """Refreshes the current satellite catalog from CelesTrak. This is a
           very data-intensive operation, and should rarely be invoked.
        """
        catpath = data.get_path('satcat.txt')
        response = requests.get(celestrak.catUrl)
        with open(catpath, 'wb') as f:
            f.write(response.content)
        with open(catpath, 'r') as f:
            self.sci = Entry.fromFile(f)
        return 'Refresh complete!'
        
    @service.isop
    def tle(self, url, args):
        """For a given SSCID, returns the most recent TLE pulled from CelesTrak.
           Eventually, we should start caching these TLEs so Kelso doesn't get
           too pissed. The URL request format will be something like:
              http://domain.com/tle/12345
              
           Eventually, it may be worth considering several possible identifiers
           to support by way of query string arguments. We may also want to fall
           back to the SSCID listing when an SSCID is not provided.
        """
        m = re.match('^/tle/(\d{5})$', url.path)
        if m:
            url = celestrak.resolveTle(m.groups()[0])
        else:
            raise Exception('I need a five-digit SSCID')
        req = requests.get(url)
        bs = bs4.BeautifulSoup(req.text, 'html.parser')
        return str(bs.pre.text).strip()
