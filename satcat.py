"""Satellite catalog interface and data models, designed around 128-character
   satellite catalog summary entries documented and used by CelesTrak:
      http://celestrak.com/satcat/satcat-format.asp.
"""

from kepler import service, data

class Entry(object):
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
    def __init__(self):
        self.sci = None
        with open(data.get_path('satcat.txt'), 'r') as f:
            self.sci = Entry.fromFile(f)
            
    def _root(self, url, args):
        res = ''
        for sc in self.sci:
            res += sc.catNum + '\n'
        return res
