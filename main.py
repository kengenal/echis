
from dotenv import load_dotenv

import echis
from echis import mongo_init
from echis.model.share import SharedSongs, get_interface

if __name__ == "__main__":
    load_dotenv()
    load_dotenv('.env.local')
    echis.start_bot()
