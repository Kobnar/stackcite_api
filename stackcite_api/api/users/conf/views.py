from mongoengine import context_managers
from pyramid.view import view_defaults

from stackcite import data as db

from stackcite_api import views, exceptions


@view_defaults(renderer='json')
class ConfirmationViews(views.BaseView):
    """``../conf/``"""

    METHODS = {
        'POST': 'create',
        'PUT': 'update',
    }

    @views.managed_view
    def create(self):
        data = self.request.json_body
        self.context.create(data)
        return exceptions.APINoContent()

    @views.managed_view
    def update(self):
        data = self.request.json_body
        conf_token = self.context.update(data)
        with context_managers.no_dereference(db.ConfirmToken):
            return {
                'user': {
                    'id': str(conf_token.user.id)
                }
            }
