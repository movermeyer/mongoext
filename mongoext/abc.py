import weakref


class AbstractField(object):
    def __init__(self, **kw):
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        value = self.cast(value)
        self.data[instance] = value

    def __delete__(self, instance):
        del self.data[instance]

    def process(self, value):
        raise NotImplementedError
