import os
import mongoengine


class UnitTestLayer(object):
    """
    The base test layer for `citeline`.
    """


class MongoIntegrationTestLayer(UnitTestLayer):
    """
    An integration test layer for working with the `citeline` database.
    """

    _IP = os.environ.get('MONGO_TEST_IP', 'http://127.0.0.1/')
    _DB = os.environ.get('MONGO_TEST_DB', 'test')
    _USER = os.environ.get('MONGO_TEST_USER', 'test')
    _PASSWORD = os.environ.get('MONGO_TEST_PASSWORD', 'test')

    @classmethod
    def setUp(cls):
        db = mongoengine.connect(
            cls._DB,
            username=cls._USER,
            password=cls._PASSWORD
        )
        db.drop_database(cls._DB)
