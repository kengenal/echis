
from dotenv import load_dotenv

import echis

if __name__ == "__main__":
    load_dotenv()
    load_dotenv('.env.local')
    echis.start_bot()
