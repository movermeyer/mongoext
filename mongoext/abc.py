import weakref


class AbstractField(object):
    def __init__(self, fields):
        self.fields = fields
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        if value is None:
            del self.data[instance]
            return

        self.data[instance] = self.fields(value)

    def __delete__(self, instance):
        del self.data[instance]
