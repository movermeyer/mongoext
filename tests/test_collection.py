import unittest

from . import fixture


class FindDocumentTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }, {
            'title': u'Title2',
            'description': u'Description2',
            'content': u'Content2',
            'created_ts': 2,
        }, {
            'title': u'Title3',
            'description': u'Description3',
            'content': u'Content3',
            'created_ts': 3,
        }]

        fixture.Collection().insert(self.documents)

    def equal(self, documents1, documents2):
        documents1 = [d for d in documents1]
        for document in documents1:
            document.pop('_id')
        self.assertEqual(documents1, documents2)

    def test_find_documents(self):
        documents = fixture.Collection().find()
        self.equal(documents, self.documents)

    def test_find_documents_by_spec(self):
        spec = {
            'created_ts': 2
        }
        documents = fixture.Collection().find(spec)
        self.equal(documents, [self.documents[1]])

    def test_find_documents_by_spec_with_empty_result(self):
        spec = {
            'created_ts': -1
        }
        documents = fixture.Collection().find(spec)
        self.equal(documents, [])

    def test_find_documents_by_spec_with_more_the_one_result(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        documents = fixture.Collection().find(spec)
        self.equal(documents, self.documents[1:])

    def test_find_documents_with_specified_fields(self):
        documents = fixture.Collection().find(fields={'created_ts': 1})
        self.equal(documents, [{'created_ts': d['created_ts']} for d in self.documents])

    def test_find_documents_with_skip(self):
        documents = fixture.Collection().find(skip=1)
        self.equal(documents, self.documents[1:])

    def test_find_documents_by_spec_with_fields_and_skip(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        fields = {'created_ts': 1}
        skip = 1
        documents = fixture.Collection().find(spec, fields, skip)
        self.equal(documents, [{'created_ts': d['created_ts']} for d in self.documents[2:]])


class FindModelsTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.models = [fixture.Model(**{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }), fixture.Model(**{
            'title': u'Title2',
            'description': u'Description2',
            'content': u'Content2',
            'created_ts': 2,
        }), fixture.Model(**{
            'title': u'Title3',
            'description': u'Description3',
            'content': u'Content3',
            'created_ts': 3,
        })]

        document_ids = fixture.Model.objects.insert(self.models)
        for document_id, model in zip(document_ids, self.models):
            model._id = document_id

    def equal(self, documents1, documents2):
        self.assertEqual([d.to_dict() for d in documents1], [d.to_dict() for d in documents2])

    def test_find_models(self):
        models = fixture.Model.objects.find()
        self.equal(models, self.models)

    def test_find_models_by_spec(self):
        spec = {
            'created_ts': 2
        }
        models = fixture.Model.objects.find(spec)
        self.equal(models, [self.models[1]])

    def test_find_models_by_spec_with_empty_result(self):
        spec = {
            'created_ts': -1
        }
        models = fixture.Model.objects.find(spec)
        self.equal(models, [])

    def test_find_models_by_spec_with_more_the_one_result(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        models = fixture.Model.objects.find(spec)
        self.equal(models, self.models[1:])

    def test_find_documents_with_skip(self):
        models = fixture.Model.objects.find(skip=1)
        self.equal(models, self.models[1:])

    def test_find_documents_by_spec_with_fields_and_skip(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        skip = 1
        models = fixture.Model.objects.find(spec, skip=skip)
        self.equal(models, self.models[2:])


class CountTestCase(fixture.MongoextTestCase):
    def setUp(self):
        pass

    def test_single_document_in_collection(self):
        documents = [{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }]

        fixture.Collection().insert(documents)
        self.assertEqual(fixture.Collection().count(), 1)

    def test_multiple_document_in_collection(self):
        documents = [{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }, {
            'title': u'Title2',
            'description': u'Description2',
            'content': u'Content2',
            'created_ts': 2,
        }, {
            'title': u'Title3',
            'description': u'Description3',
            'content': u'Content3',
            'created_ts': 3,
        }]

        fixture.Collection().insert(documents)
        self.assertEqual(fixture.Collection().count(), 3)


class DistinctTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
        }, {
            'title': u'Title',
        }, {
            'title': u'Title1',
        }]
        fixture.Collection().insert(self.documents)

    def test_distinct(self):
        self.assertEqual(fixture.Collection().distinct('title'), [u'Title', u'Title1'])


class DropTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
        }, {
            'title': u'Title',
        }, {
            'title': u'Title1',
        }]
        fixture.Collection().insert(self.documents)

    def test_drop(self):
        self.assertIsNone(fixture.Collection().drop())

    def test_multiple_drop(self):
        fixture.Collection().drop()
        fixture.Collection().drop()
        self.assertIsNone(fixture.Collection().drop())


class EmptyCollectionTestCase(unittest.TestCase):
    def test_collection_count(self):
        pass
