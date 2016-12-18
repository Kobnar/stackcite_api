from stackcite import data as db

from stackcite_api import resources

from . import schema


class PersonDocument(resources.APIDocument):

    _SCHEMA = {
        'PUT': schema.UpdatePerson
    }


class PersonCollection(resources.APICollection):

    _SCHEMA = {
        'POST': schema.CreatePerson
    }

    _COLLECTION = db.Person
    _DOCUMENT_RESOURCE = PersonDocument
