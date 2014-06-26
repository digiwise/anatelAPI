import datetime
from google.appengine.ext import ndb
from google.appengine.tools import bulkloader
import models


class ExecutiveDirectorsLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'ExecutiveDirectors',

                                   [('directorName', str),
                                    ('directorPhotoKey', str),
                                    ('publication_date',
                                     lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
                                    ('length_in_minutes', int)
                                   ])


loaders = [ExecutiveDirectorsLoader]

"""
    directorName = ndb.StringProperty(required=True)
    directorPhotoKey = ndb.BlobKeyProperty()
    placeOfBirth = ndb.StringProperty()
    mandateStart = ndb.DateProperty()
    mandateEnd = ndb.DateProperty()
    appointment = ndb.IntegerProperty(required=True)
    biography = ndb.TextProperty(compressed=True)
    refLinks = ndb.JsonProperty(compressed=True)
    politicalPartyAffinity = ndb.JsonProperty(compressed=False)
"""