from . import fixture


class Cursor(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }, {
            'title': u'Title0',
            'description': u'Description0',
            'content': u'Content',
            'created_ts': 0,
        }, {
            'title': u'Title2',
            'description': u'Description2',
            'content': u'Content2',
            'created_ts': 2,
        }]

        fixture.Collection().insert(self.documents)

    def equal(self, documents1, documents2):
        documents1 = [d for d in documents1]
        for document in documents1:
            document.pop('_id')
        self.assertEqual(documents1, documents2)

    def test_sort(self):
        documents = fixture.Collection().find().sort('created_ts')
        expected = [self.documents[1], self.documents[0], self.documents[2]]
        self.equal(documents, expected)

    def test_count(self):
        documents = fixture.Collection().find({'content': u'Content'}).count()
        self.assertEqual(documents, 2)

    def test_distinct(self):
        values = fixture.Collection().find().distinct('content')
        self.assertEqual(values, [u'Content', u'Content2'])

    def test_limit(self):
        documents = fixture.Collection().find().sort('created_ts').limit(1)
        self.equal(documents, [self.documents[1]])

    def test_rewind(self):
        cursor = fixture.Collection().find()
        next(cursor)
        cursor.rewind()
        self.equal(cursor, self.documents)

    def test_skip(self):
        documents = fixture.Collection().find().skip(1)
        self.equal(documents, self.documents[1:])
