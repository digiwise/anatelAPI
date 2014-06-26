from protorpc import messages


class ExecutiveDirectorsPutRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent a Executive Director to be inserted
    """

    directorName = messages.StringField(1, required=True)
    directorPhotoKey = messages.BytesField(2, required=False)
    placeOfBirth = messages.StringField(3, required=True)
    mandates = messages.StringField(4, required=True)
    appointment = messages.IntegerField(5, required=True)
    biography = messages.StringField(6, required=True)
    refLinks = messages.StringField(7, required=True)
    politicalPartyAffinity = messages.StringField(8, required=True)


class ExecutiveDirectorsUpdateRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent a Executive Director to be inserted
    """

    directorKey = messages.StringField(1, required=True)
    directorName = messages.StringField(2, required=True)
    directorPhotoKey = messages.BytesField(3, required=False)
    placeOfBirth = messages.StringField(4, required=True)
    mandates = messages.StringField(5, required=True)
    appointment = messages.IntegerField(6, required=True)
    biography = messages.StringField(7, required=True)
    refLinks = messages.StringField(8, required=True)
    politicalPartyAffinity = messages.StringField(9, required=True)


class EDProfessionalHistoryPutRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent a professional history entry to be inserted
    for a Executive Director
    """

    directorKey = messages.StringField(1, required=True)
    institutionName = messages.StringField(2, required=True)
    position = messages.StringField(3, required=True)
    admissionDate = messages.StringField(4, required=True)
    exitDate = messages.StringField(5, required=True)
    poControl = messages.BooleanField(6, required=True)
    piControl = messages.BooleanField(7, required=True)


class EDProfessionalHistoryUpdateRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent a professional history entry to be updated
    for a Executive Director
    """

    directorKey = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    institutionName = messages.StringField(3, required=True)
    position = messages.StringField(4, required=True)
    admissionDate = messages.StringField(5, required=True)
    exitDate = messages.StringField(6, required=True)
    poControl = messages.BooleanField(7, required=True)
    piControl = messages.BooleanField(8, required=True)


class EDSuccessResponseMessage(messages.Message):
    """
    ProtoRPC message definition to represent a response to a Executive Director Put or Update response
    """

    entityKey = messages.StringField(1, required=True)
    serverResponse = messages.StringField(2, required=True)


class ExecutiveDirectorsGetRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent the filter used to query for the Executive Directors
    filter => FHC(1), Lula(2), Dilma(3)
    """

    filter = messages.StringField(1, required=True, default='[1,2,3]')


class ExecutiveDirectorsGetResponseMessage(messages.Message):
    """
    ProtoRPC message definition to represent the a response GetExecutiveDirectorsRequestMessage,that returns a json
    containing a list of directors and the details of each one.
    """

    queryResult = messages.StringField(1, required=True)


class ExecutiveDirectorGetRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent the key for the Executive Director entity
    """

    directorId = messages.IntegerField(1, required=True, default=0)


class ExecutiveDirectorGetResponseMessage(messages.Message):
    """
    ProtoRPC message definition to represent the response to GetExecutiveDirectorRequestMessage as a
    Json containing the details about a given director
    """

    queryResult = messages.StringField(1, required=True)


class EDProfessionalHistoryGetRequestMessage(messages.Message):
    """
    ProtoRPC message definition to represent the request for the professional history from a given
    Executive Director
    """

    directorKey = messages.StringField(1, required=True)


class EDProfessionalHistoryGetResponseMessage(messages.Message):
    """
    ProtoRPC message definition to represent the EDProfessionalHistoryGetRequestMessage response
    containing the professional history of an Executive Director
    """

    directorKey = messages.StringField(1, required=True)
    professionalHistory = messages.StringField(2, required=True)


class BlobRequestMessage(messages.Message):
    """
        ProtoRPC message definition to represent a Blob URL request.
    """

    type = messages.StringField(1, required=False)


class BlobResponseMessage(messages.Message):
    """
        ProtoRPC message definition to represent a Blob URL request.
    """

    blobResponseString = messages.StringField(1, required=True)
    blobResponseType = messages.StringField(2, required=True)