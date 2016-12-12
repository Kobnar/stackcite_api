import unittest

from citeline_api import testing


def make_person(data, save=False):
    from citeline.data import Person
    person = Person()
    person.deserialize(data)
    if save:
        person.save()
    return person


class PersonCollectionIntegrationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from citeline.data import Person
        Person.drop_collection()
        from ..resources import PersonCollection
        self.collection = PersonCollection(None, 'people')


class PersonCollectionCreateTestCase(PersonCollectionIntegrationTestCase):

    def test_create_valid_person_returns_dict_with_id(self):
        """PersonCollection.create() returns a dictionary with an ObjectId
        """
        data = {'name': {'full': 'John Nobody Doe'}}
        result = self.collection.create(data)
        self.assertIsNotNone(result['id'])

    def test_create_invalid_person_raises_exception(self):
        """PersonCollection.create() raises ValidationError for invalid data
        """
        from marshmallow import ValidationError
        data = {'name': {'first': 'John', 'full': 'John Nobody Doe'}}
        with self.assertRaises(ValidationError):
            self.collection.create(data)


class PersonCollectionRetrieveTestCase(PersonCollectionIntegrationTestCase):

    def test_retrieve_people_returns_all_people(self):
        """PersonCollection.retrieve() returns ObjectIds for everybody in the database
        """
        from citeline.testing.data import people as ppl
        people = [make_person(p, save=True) for p in ppl()]
        results = [r['id'] for r in self.collection.retrieve()]
        for pid in people:
            expected = str(pid.id)
            self.assertIn(expected, results)


class PersonDocumentIntegrationTestCase(PersonCollectionIntegrationTestCase):

    def setUp(self):
        super().setUp()
        from random import randint
        from citeline.testing.data import people as ppl
        people = ppl()
        rand_idx = randint(0, len(people) - 1)
        person = make_person(people[rand_idx], save=True)
        self.document = self.collection[person.id]


class PersonDocumentRetrieveTestCase(PersonDocumentIntegrationTestCase):

    def test_retrieve_returns_person(self):
        """PersonDocument.retrieve() returns data with the correct ObjectId
        """
        expected = str(self.document.id)
        result = self.document.retrieve()['id']
        self.assertEqual(expected, result)


class PersonDocumentUpdateTestCase(PersonDocumentIntegrationTestCase):

    def test_update_returns_updated_data(self):
        """PersonDocument.update() returns a dict of updated data
        """
        expected = 'Updated Person'
        data = {'name': {'title': expected}}
        result = self.document.update(data)['name']['title']
        self.assertEqual(expected, result)

    def test_update_with_invalid_data_raises_exception(self):
        """PersonDocument.update() raises ValidationError with invalid data
        """
        from marshmallow import ValidationError
        data = {'name': {'first': 'John', 'full': 'John Nobody Doe'}}
        with self.assertRaises(ValidationError):
            self.document.update(data)