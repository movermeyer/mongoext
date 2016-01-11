class ICollection(object):
    def __init__(self, collection):
        self.collection = collection

    def find(self, filter_=None, projection=None, skip=0):
        raise NotImplementedError

    def find_one(self, filter_or_id=None, *args, **kw):
        raise NotImplementedError

    def find_one_and_replace(self, filter_, replacement, projection=None):
        raise NotImplementedError

    def insert(self, documents):
        raise NotImplementedError

    def insert_one(self, document):
        raise NotImplementedError

    def save(self, document):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def distinct(self, field):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def remove(self, spec=None, multi=True):
        raise NotImplementedError

    def update(self, spec, document, multi=False):
        raise NotImplementedError


class ICursor(object):
    def __init__(self, cursor):
        self.cursor = cursor

    def sort(self, field):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def distinct(self, field):
        raise NotImplementedError

    def limit(self, limit):
        raise NotImplementedError

    def rewind(self):
        raise NotImplementedError

    def skip(self, skip):
        raise NotImplementedError
