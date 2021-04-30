import mongoengine as me

from datetime import datetime


class FilterModel(me.Document):
    name = me.StringField(required=True, unique=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
