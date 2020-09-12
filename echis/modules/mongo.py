import os

from mongoengine import connect


def mongo_init(test: bool = False):
    if test:
        return connect('mongoenginetest', host='mongomock://localhost')
    mongo = os.getenv("MONGO_URL")
    return connect(host=str(mongo))
