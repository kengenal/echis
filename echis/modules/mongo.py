import os

from mongoengine import connect

from echis.main.settings import MONGO_URL


def mongo_init(test: bool = False):
    if test:
        return connect('mongoenginetest', host='mongomock://localhost')
    mongo = MONGO_URL
    return connect(host=str(mongo))
