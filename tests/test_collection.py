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
        documents = fixture.Collection().find(projection={'created_ts': 1})
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

    def test_find_one_document(self):
        document = fixture.Collection().find_one({'created_ts': 1})
        # print [d for d in fixture.Collection().find({'created_ts': 1})]
        self.equal([document], [self.documents[0]])

    def test_find_one_document_for_none_results(self):
        document = fixture.Collection().find_one({'created_ts': -1})
        self.assertIsNone(document)

    def test_find_one_document_for_multiple_results(self):
        document = fixture.Collection().find_one()
        self.equal([document], [self.documents[0]])


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


class RemoveTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
        }, {
            'title': u'Title',
        }, {
            'title': u'Title1',
        }]
        fixture.Collection().insert(self.documents)

    def test_complete_remove(self):
        fixture.Collection().remove()
        self.assertEqual(fixture.Collection().count(), 0)

    def test_single_removal(self):
        fixture.Collection().remove({'title': u'Title1'})
        self.assertEqual(fixture.Collection().count(), 2)

    def test_multiple_removal(self):
        fixture.Collection().remove({'title': u'Title'})
        self.assertEqual(fixture.Collection().count(), 1)

    def test_multiple_removal_with_multi_false(self):
        fixture.Collection().remove({'title': u'Title'}, multi=False)
        self.assertEqual(fixture.Collection().count(), 2)


class UpdateTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.documents = [{
            'title': u'Title',
        }, {
            'title': u'Title',
        }, {
            'title': u'Title1',
        }]
        fixture.Collection().insert(self.documents)

    def test_update_one(self):
        fixture.Collection().update({'title': u'Title'}, {'$set': {'title': u'Title2'}})
        documents = [d for d in fixture.Collection().find({'title': u'Title2'})]
        self.assertEqual(len(documents), 1)

    def test_update_multi(self):
        fixture.Collection().update({'title': u'Title'}, {'$set': {'title': u'Title2'}}, multi=True)
        documents = [d for d in fixture.Collection().find({'title': u'Title2'})]
        self.assertEqual(len(documents), 2)


class SaveDocumentTestCase(fixture.MongoextTestCase):
    def setUp(self):
        pass

    def test_save_new_document(self):
        document = {
            'title': u'Title',
        }
        fixture.Collection().save(document)
        self.assertEqual(fixture.Collection().count(), 1)

    def test_save_existed_document(self):
        document = {'title': u'Title'}
        _id = fixture.Collection().save(document)
        document['_id'] = _id
        document['title'] = u'Title1'
        fixture.Collection().save(document)
        self.assertEqual(fixture.Collection().count(), 1)


class NoCompressionCollection(fixture.Collection):
    FIELDS_MAPPING = None


class Compression(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        NoCompressionCollection().drop()

    def test_pack(self):
        document = fixture.Collection.pack_document({'title': 1})
        expected = {'t': 1}
        self.assertEqual(document, expected)

    def test_unpack(self):
        document = fixture.Collection.unpack_document({'t': 1})
        expected = {'title': 1}
        self.assertEqual(document, expected)

    def test_no_compression_pack(self):
        spec = {'field': 1}
        compressed = NoCompressionCollection().pack_document(spec)
        self.assertEqual(spec, compressed)

    def test_no_compression_unpack(self):
        compressed = {'f': 1}
        spec = NoCompressionCollection().unpack_document(compressed)
        self.assertEqual(spec, compressed)

    def test_database(self):
        self.assertIsNotNone(NoCompressionCollection.database)


class FindModelsTestCase(fixture.MongoextTestCase):
    def setUp(self):
        self.models = [fixture.Document(**{
            'title': u'Title',
            'description': u'Description',
            'content': u'Content',
            'created_ts': 1,
        }), fixture.Document(**{
            'title': u'Title2',
            'description': u'Description2',
            'content': u'Content2',
            'created_ts': 2,
        }), fixture.Document(**{
            'title': u'Title3',
            'description': u'Description3',
            'content': u'Content3',
            'created_ts': 3,
        })]

        document_ids = fixture.Collection(fixture.Document).insert(self.models)
        for document_id, model in zip(document_ids, self.models):
            model._id = document_id

    def equal(self, documents1, documents2):
        self.assertEqual([dict(d) for d in documents1], [dict(d) for d in documents2])

    def test_find_models(self):
        models = fixture.Collection(fixture.Document).find()
        self.equal(models, self.models)

    def test_find_models_by_spec(self):
        spec = {
            'created_ts': 2
        }
        models = fixture.Collection(fixture.Document).find(spec)
        self.equal(models, [self.models[1]])

    def test_find_models_by_spec_with_empty_result(self):
        spec = {
            'created_ts': -1
        }
        models = fixture.Collection(fixture.Document).find(spec)
        self.equal(models, [])

    def test_find_models_by_spec_with_more_the_one_result(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        models = fixture.Collection(fixture.Document).find(spec)
        self.equal(models, self.models[1:])

    def test_find_documents_with_skip(self):
        models = fixture.Collection(fixture.Document).find(skip=1)
        self.equal(models, self.models[1:])

    def test_find_documents_by_spec_with_fields_and_skip(self):
        spec = {
            'created_ts': {'$gt': 1},
        }
        skip = 1
        models = fixture.Collection(fixture.Document).find(spec, skip=skip)
        self.equal(models, self.models[2:])


class SaveModelTestCase(fixture.MongoextTestCase):
    def setUp(self):
        pass

    def test_save_new_model(self):
        model = fixture.Document(**{
            'created_ts': 1,
        })
        fixture.Collection(fixture.Document).save(model)
        self.assertEqual(fixture.Collection().count(), 1)

    # def test_save_existed_model(self):
    #     model = fixture.Document(**{
    #         'created_ts': 1,
    #     })
    #     _id = fixture.Collection(fixture.Document).save(model)
    #     # assert False, (model.get('_id'), model._id, model['_id'])
    #     model._id = _id
    #     model.created_ts = 2
    #     fixture.Collection(fixture.Document).save(model)
    #     self.assertEqual(fixture.Collection(fixture.Document).count(), 1)
