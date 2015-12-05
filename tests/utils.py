import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def get_connection():
    mongo = os.getenv('MONGO')
    if not mongo:
        raise RuntimeError('Please provide MONGO env variable with mongodb dsn')
    mongo = urlparse.urlparse(mongo)
    try:
        host, port = mongo.netloc.split(':', 1)
    except ValueError:
        host = mongo.netloc
        port = 27017
    else:
        port = int(port)

    return {'host': host, 'port': port}
