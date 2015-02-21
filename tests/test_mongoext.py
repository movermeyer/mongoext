from . import fixture


class Mongoext(fixture.MongoextTestCase):
    def test_model_find(self):
        cursor = fixture.Model.objects.find({'about': {'$gte': 1}}, {'about': 1}).sort('about')
        self.assertTrue(all([lambda: isinstance(c, fixture.Model) for c in cursor]))

    def test_model_save(self):
        cursor = fixture.Model.objects.find({'about': {'$gte': 1}}, {'about': 1}).sort('about')
        model = [c for c in cursor][0]
        model.save()

    def test_model_fail_save(self):
        cursor = fixture.Model.objects.find({'about': {'$gte': 1}}, {'about': 1}).sort('about')
        model = [c for c in cursor][0]
        model.about = None
        with self.assertRaises(TypeError):
            model.save()

    def test_model_fail_insert(self):
        with self.assertRaises(TypeError):
            fixture.Model.objects.insert(True)
