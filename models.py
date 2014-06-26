import datetime
import endpoints
from google.appengine.ext import ndb
import logging
import json

from google.appengine.ext.ndb import blobstore

from anatel_api_messages import BlobResponseMessage
from anatel_api_messages import EDSuccessResponseMessage, ExecutiveDirectorGetResponseMessage
from anatel_api_messages import ExecutiveDirectorsGetResponseMessage
from anatel_api_messages import EDProfessionalHistoryGetResponseMessage

TIME_FORMAT_STRING = '%d/%m/%Y'


class ExecutiveDirectors(ndb.Expando):
    """
    Models the Anatel Executive Directors Border
    Root Property
    """
    directorName = ndb.StringProperty(required=True)
    directorPhotoKey = ndb.StringProperty()
    placeOfBirth = ndb.StringProperty()
    mandates = ndb.JsonProperty(required=True)
    appointment = ndb.IntegerProperty(required=True)
    biography = ndb.TextProperty(compressed=False)
    refLinks = ndb.JsonProperty(required=False)
    politicalPartyAffinity = ndb.StringProperty(compressed=False)

    @property
    def timestamp(self):
        """
            Property to format a datetime object to string.
        """
        return self.join_date.strftime(TIME_FORMAT_STRING)

    def to_message(self):

        query_result = {'directorId': self.key.id(),
                        'directorName': self.directorName,
                        'directorPhotoKey': self.directorPhotoKey,
                        'placeOfBirth': self.placeOfBirth,
                        'mandates': self.mandates,
                        'appointment': self.appointment,
                        'biography': self.biography,
                        'refLinks': self.refLinks,
                        'politicalPartyAffinity': self.politicalPartyAffinity}

        return ExecutiveDirectorGetResponseMessage(queryResult=json.dumps(query_result))


    def to_success_message(self):
        return EDSuccessResponseMessage(entityKey=self.key.id(),
                                        serverResponse=self.serverResponse
        )

    @staticmethod
    def directors_to_message(directors):
        #logging.getLogger().setLevel(logging.INFO)
        #logging.info('%s' % directors)

        computed_directors = []
        for director in directors:
            #logging.info('%s' % director)
            director_dict = {'directorId': director.key.id(),
                             'directorName': director.directorName,
                             'directorPhotoKey': director.directorPhotoKey,
                             'placeOfBirth': director.placeOfBirth,
                             'mandates': json.dumps(director.mandates),
                             'appointment': director.appointment,
                             'biography': director.biography,
                             'refLinks': json.dumps(director.refLinks),
                             'politicalPartyAffinity': director.politicalPartyAffinity}
            computed_directors.append(director_dict)

        message_json = json.dumps(computed_directors, sort_keys=False, indent=0)

        #logging.info('message_json')
        #logging.info('%s' % computed_directors.__str__())
        return ExecutiveDirectorsGetResponseMessage(queryResult=message_json)

    @staticmethod
    def to_director_message(data):
        return json.dumps(data, sort_keys=True, indent=4)

    @classmethod
    def get_directors(cls, message):
        #logging.info(message.filter)

        directors_filters = json.loads(message.filter)
        if not directors_filters:
            directors_filters = [0]
        q = cls.query()
        q = q.filter(cls.appointment.IN(directors_filters))
        q = q.order(cls.directorName)

        return q.fetch(100)

    @classmethod
    def get_director(cls, message):

        director_id = message.directorId
        return cls.get_by_id(director_id)


class ProfessionalHistory(ndb.Expando):
    """
    Models the Executive Director's professional history
    ExecutiveDirectors child

    poControl => position was taken after mandate at Anatel?
    piControl => is this a private company?
    """
    institutionName = ndb.StringProperty(required=True)
    position = ndb.StringProperty(required=True)
    admissionDate = ndb.DateProperty(required=True)
    exitDate = ndb.DateProperty(required=True)
    poControl = ndb.BooleanProperty(required=True)
    piControl = ndb.BooleanProperty(required=True)

    def to_history_message(self):
        return EDProfessionalHistoryGetResponseMessage(directorKey=self.directorKey,
                                                       entityKey=self.key.id(),
                                                       professionalHistory=self.professionalHistory)


class BlobProcessing(ndb.Model):
    """
        property to processes a blob upload steps
    """

    blob_response_string = ndb.StringProperty(required=True)
    blob_response_type = ndb.StringProperty(required=True)

    def to_message(self):
        return BlobResponseMessage(
            blobResponseString=self.blob_response_string,
            blobResponseType=self.blob_response_type
        )

    @classmethod
    def get_upload_url(cls, message):
        blob_upload_url = blobstore.create_upload_url('/directors')

        resp = cls(
            blob_response_type=message.type,
            blob_response_string=blob_upload_url
        )

        return resp