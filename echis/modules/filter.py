import csv

def is_bad_word(word: str, path: str = None) -> bool:
    is_bad = False
    with open(path, 'r') as f:
        my_content = csv.reader(f, delimiter='\n')
        for row in my_content:
            if word in row:
                is_bad = True
    return is_bad
