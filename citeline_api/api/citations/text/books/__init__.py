from . import resources, views, schemas


def traversal_factory(parent, name):
    sources = resources.BookCitationCollection(parent, name)
    return sources
