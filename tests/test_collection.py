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

    def test_find_documents(self):
        documents = [d for d in fixture.Collection().find()]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, self.documents)

    def test_find_documents_by_spec(self):
        spec = {
            'created_ts': 2
        }
        documents = [d for d in fixture.Collection().find(spec)]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, [self.documents[1]])

    def test_find_documents_by_spec_with_empty_result(self):
        spec = {
            'created_ts': -1
        }
        documents = [d for d in fixture.Collection().find(spec)]
        self.assertEqual(documents, [])

    def test_find_documents_by_spec_with_more_the_one_result(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        documents = [d for d in fixture.Collection().find(spec)]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, self.documents[1:])

    def test_find_documents_with_specified_fields(self):
        documents = [d for d in fixture.Collection().find(fields={'created_ts': 1})]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, [{'created_ts': d['created_ts']} for d in self.documents])

    def test_find_documents_with_skip(self):
        documents = [d for d in fixture.Collection().find(skip=1)]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, self.documents[1:])

    def test_find_documents_by_spec_with_fields_and_skip(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        fields = {'created_ts': 1}
        skip = 1
        documents = [d for d in fixture.Collection().find(spec, fields, skip)]
        for document in documents:
            document.pop('_id')
        self.assertEqual(documents, [{'created_ts': d['created_ts']} for d in self.documents[2:]])


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


class EmptyCollectionTestCase(unittest.TestCase):
    def test_collection_count(self):
        pass
