import os
from dotenv import load_dotenv

load_dotenv()

EXAMPLE=os.getenv('EXAMPLE')
SECOND_EXAMPLE=os.getenv('SECOND_EXAMPLE')

print(EXAMPLE)
print(SECOND_EXAMPLE)