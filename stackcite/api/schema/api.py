from marshmallow import Schema, fields as mm_fields, validates, ValidationError

from . import fields as api_fields


API_METHODS = ('POST', 'GET', 'PUT', 'DELETE')


class APISchema(Schema):
    """
    A default schema class that stores a "method" context, used to enforce
    method-specific requirements on an API schema.
    """

    def __init__(self, method=None, *args, **kwargs):

        assert not method or method in API_METHODS

        super().__init__(*args, **kwargs)
        self.context['method'] = method

    @property
    def method(self):
        return self.context['method']


class RetrieveCollection(Schema):
    """
    A default validation schema class to RETRIEVE documents from a MongoDB
    collection

    By default, schema sets both `limit=100` and `skip=0` to avoid massive
    database dumps.
    """

    ids = api_fields.ListField(api_fields.ObjectIdField)
    fields = api_fields.FieldsField()
    limit = mm_fields.Integer(missing=100)
    skip = mm_fields.Integer(missing=0)

    @validates('limit')
    def validate_limit(self, value):
        if value < 1:
            msg = '"limit" must be >= 1 ({})'.format(value)
            raise ValidationError(msg)

    @validates('skip')
    def validate_skip(self, value):
        if value < 0:
            msg = '"skip" must be >= 0 ({})'.format(value)
            raise ValidationError(msg)


class RetrieveDocument(Schema):
    fields = api_fields.FieldsField()