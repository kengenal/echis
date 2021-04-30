import random
import uuid
from datetime import datetime

import factory
from factory import Faker

from echis.model.filter_model import FilterModel


class FilterFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = FilterModel

    name = Faker("name")
    created_at = factory.Sequence(lambda n: datetime.utcnow)

