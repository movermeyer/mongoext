from . import fixture


class ModelTestCase(fixture.MongoextTestCase):
    def test_find(self):
        cursor = fixture.Document.objects.find({'created_ts': {'$gte': 1}}, {'title': 1}).sort('created_ts')
        self.assertTrue(all([lambda: isinstance(c, fixture.Document) for c in cursor]))

    def test_save(self):
        cursor = fixture.Document.objects.find({'created_ts': {'$gte': 1}}).sort('created_ts')
        model = [c for c in cursor][0]
        model.save()

    def test_fail_save(self):
        cursor = fixture.Document.objects.find({'created_ts': {'$gte': 1}}, {'title': 1}).sort('created_ts')
        model = [c for c in cursor][0]
        model.created_ts = None
        with self.assertRaises(ValueError):
            model.save()

    def test_fail_insert(self):
        with self.assertRaises(TypeError):
            fixture.Document.objects.insert_one(True)

    def test_repr(self):
        model = fixture.Document.objects.find_one()
        self.assertTrue(isinstance(repr(model), basestring))
