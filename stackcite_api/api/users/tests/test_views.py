from stackcite_api import testing


class ConfirmationViewsTestCase(testing.views.ViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    from ..resources import ConfirmationResource
    RESOURCE_CLASS = ConfirmationResource

    from ..views import ConfirmationViews
    VIEW_CLASS = ConfirmationViews

    def setUp(self):
        from stackcite import data as db
        db.User.drop_collection()
        db.ConfirmToken.drop_collection()
        super().setUp()


class ConfirmationViewsCreateTestCase(ConfirmationViewsTestCase):

    def test_create_creates_confirmation_token(self):
        """ConfirmationViews.create() creates ConfirmationToken in database
        """
        view = self.get_view()
        email = 'test@email.com'
        password = 'T3stPa$$word'
        from stackcite import data as db
        user = db.User.new(email, password, save=True)
        view.request.json_body = {'email': email}
        view.create()
        import mongoengine
        try:
            db.ConfirmToken.objects.get(_user=user)
        except mongoengine.DoesNotExist as err:
            msg = 'ConfirmationToken does not exist: {}'.format(err)
            self.fail(msg=msg)


class ConfirmationViewsUpdateTestCase(ConfirmationViewsTestCase):

    def setUp(self):
        super().setUp()
        from stackcite import data as db
        self.user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        self.token = db.ConfirmToken.new(self.user, save=True)

    def test_update_deletes_confirmation_token(self):
        """ConfirmationViews.update() deletes ConfirmationToken in database
        """
        view = self.get_view()
        view.request.json_body = {'key': self.token.key}
        view.update()
        import mongoengine
        from stackcite import data as db
        with self.assertRaises(mongoengine.DoesNotExist):
            db.ConfirmToken.objects.get(_key=self.token.key)

    def test_update_confirms_user(self):
        """ConfirmationViews.update() confirms associated user
        """
        view = self.get_view()
        view.request.json_body = {'key': self.token.key}
        view.update()
        self.user.reload()
        self.assertIsNotNone(self.user.confirmed)