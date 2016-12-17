import unittest

from stackcite_api import testing


class UpdateOrganizationTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import UpdateOrganization
        self.schema = UpdateOrganization()


class CreateOrganizationTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import CreateOrganization
        self.schema = CreateOrganization()

    def test_name_required(self):
        """CreateOrganization fails if no name is provided
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('name', result)


class UpdatePublisherTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import UpdatePublisher
        self.schema = UpdatePublisher()

    def test_region_fails_single_letter(self):
        """UpdatePublisher fails a region with a single letter
        """
        data = {'region': 'A'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('region', result)

    def test_region_fails_three_letters(self):
        """UpdatePublisher fails a region with three letters
        """
        data = {'region': 'ABC'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('region', result)


class CreatePublisherTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import CreatePublisher
        self.schema = CreatePublisher()

    def test_name_required(self):
        """CreatePublisher fails if no name is provided
        """
        result = self.schema.load({}).errors.keys()
        self.assertIn('name', result)

    def test_region_fails_single_letter(self):
        """CreatePublisher fails a region with a single letter
        """
        data = {'region': 'A'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('region', result)

    def test_region_fails_three_letters(self):
        """CreatePublisher fails a region with three letters
        """
        data = {'region': 'ABC'}
        result = self.schema.load(data).errors.keys()
        self.assertIn('region', result)