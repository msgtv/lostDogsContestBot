import os

import dotenv
from pathlib import Path

from src.utils import create_dir_if_not_exists

MODE = 'ENV'
BASE_DIR = './'

if MODE == 'ENV':
    BASE_DIR = Path(__file__).resolve().parent.parent

    ENV_FILE = BASE_DIR / r'.env'
    DATA_DIR = BASE_DIR / 'data'
else:
    ENV_FILE = './.env'
    DATA_DIR = os.path.join(BASE_DIR, 'data')

if not os.path.isfile(ENV_FILE):
    print(f'Не найден файл .env ({ENV_FILE})')
    exit()

dotenv.load_dotenv(ENV_FILE)

# aiogram
API_TOKEN = os.getenv('API_TOKEN')
OWNER_ID = os.getenv('OWNER_CHAT_ID')
EXPIRE_DATETIME = os.getenv('EXPIRE_DATETIME')

# Создать папки, если не существуют
for d in (
        DATA_DIR,
):
    create_dir_if_not_exists(d)

DATA_FILENAME = 'contest_data'

DATA_DF = None
