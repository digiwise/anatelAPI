import random
import re
import json

import logging
import endpoints
from protorpc import remote
from protorpc import messages
from protorpc import message_types

from anatel_api_messages import ExecutiveDirectorsPutRequestMessage
from anatel_api_messages import ExecutiveDirectorsUpdateRequestMessage
from anatel_api_messages import EDSuccessResponseMessage
from anatel_api_messages import BlobRequestMessage, BlobResponseMessage
from anatel_api_messages import ExecutiveDirectorsGetRequestMessage, ExecutiveDirectorGetRequestMessage
from anatel_api_messages import ExecutiveDirectorsGetResponseMessage, ExecutiveDirectorGetResponseMessage
from anatel_api_messages import EDProfessionalHistoryGetResponseMessage

from models import ExecutiveDirectors, ProfessionalHistory, BlobProcessing


WEB_CLIENT_ID = '730063120562-gh9oodgu4b7k67n9olkqqs02msam3ve4.apps.googleusercontent.com'

DIRECTORS = endpoints.ResourceContainer(
    message_types.VoidMessage,
    filter=messages.StringField(1, variant=messages.Variant.STRING, required=True)
)

DIRECTOR = endpoints.ResourceContainer(
    message_types.VoidMessage,
    directorId=messages.IntegerField(1, variant=messages.Variant.INT32, required=True)
)

PROFESSIONAL_HISTORY = endpoints.ResourceContainer(
    directorKey=messages.StringField(1, variant=messages.Variant.STRING, required=True),
    professionalHistory=messages.StringField(2, variant=messages.Variant.STRING, required=True)
)

@endpoints.api(name='anatel', version='v1')
class AnatelApi(remote.Service):

    @staticmethod
    def gql_json_parser(query_obj):
        result = []
        for entry in query_obj:
            result.append(dict([(p, unicode(getattr(entry, p))) for p in entry.properties()]))
        return result

    @endpoints.method(DIRECTORS, ExecutiveDirectorsGetResponseMessage,
                      path='directors/{filter}', http_method='POST',
                      name='directors.listDirectors')
    def directors_list(self, request):
        logging.info(request)
        directors_list = ExecutiveDirectors.get_directors(request)
        if directors_list is None:
            raise endpoints.NotFoundException('No directors found')
        return ExecutiveDirectors.directors_to_message(directors_list)

    @endpoints.method(DIRECTOR, ExecutiveDirectorGetResponseMessage,
                      path='director/{directorId}', http_method='GET',
                      name='director.get')
    def director_get(self, request):
        entity = ExecutiveDirectors.get_director(request)
        if entity is None:
            raise endpoints.NotFoundException('%s is not a user!' % request.id)
        return entity.to_message()


APP = endpoints.api_server([AnatelApi],
                           restricted=False)