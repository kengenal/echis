import csv

import mongoengine as me

from datetime import datetime

from echis.main import settings


class FilterModel(me.Document):
    name = me.StringField(required=True, unique=True)
    created_at = me.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def generate_csv() -> None:
        """ get words from database and create csv file """
        if words := FilterModel.objects:
            with open(settings.FILTER, 'w', newline='') as file:
                for i in words:
                    writer = csv.writer(file)
                    writer.writerow([i.name])
