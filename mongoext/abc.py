import weakref


class AbstractField(object):
    def __init__(self, descriptors):
        self.descriptors = descriptors
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        self.data[instance] = value

    def __delete__(self, instance):
        del self.data[instance]
