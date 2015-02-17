import mongoext.fields
import mongoext.collection
import mongoext.models


class MyCollection(mongoext.collection.Collection):
    CONNECTION = {'host': 'localhost', 'port': 27017}
    DATABASE = 'db1'
    NAME = 'collection1'

    KEY_COMPRESSION = {
        'about': 'a'
    }


class MyModel(mongoext.models.Model):
    objects = MyCollection()

    about = mongoext.fields.Numeric()


if __name__ == '__main__':
    cursor = MyCollection().find({'about': {'$gte': 1}}, {'about': 1}, 1).sort('about')
    print [c for c in cursor]
    cursor = MyModel.objects.find({'about': {'$gte': 1}}, {'about': 1}, 1).sort('about')
    print [c for c in cursor]

