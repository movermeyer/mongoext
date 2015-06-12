import unittest

import mongoext.document as document
import mongoext.schema as schema


class Document(document.Document):
    content = schema.String()
    client_id = schema.Integer() & schema.Required()


class TestInitialization(unittest.TestCase):
    def test_full_success(self):
        Document(client_id=1, content='content')

    def test_partial_success(self):
        Document(content='content')

    def test_undefined_field(self):
        Document(user_id=1)

    def test_empty_initialization(self):
        Document()
