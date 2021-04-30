import csv
import os

from echis.main import settings


def is_bad_word(word: str) -> bool:
    is_bad = False
    path = settings.FILTER
    if not os.path.exists(path):
        return is_bad
    with open(path, 'r') as f:
        my_content = csv.reader(f, delimiter='\n')
        for row in my_content:
            if word in row:
                is_bad = True
    return is_bad
