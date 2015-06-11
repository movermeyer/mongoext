class MongoextException(Exception):
    pass


class ValidationError(MongoextException):
    pass


class SchemaError(MongoextException):
    pass
