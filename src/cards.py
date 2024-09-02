import pytz
from datetime import datetime
from collections import namedtuple

from src.settings import EXPIRE_DATETIME

LostDogsCard = namedtuple('LostDogsCard', ('number', 'title'))

QUESTION = 'Как победить гиганта?'

cards = [
    LostDogsCard(number=1, title='Обманом'),
    LostDogsCard(number=2, title='Своим гигантом'),
    LostDogsCard(number=3, title='Фейрверки'),
]

# Создание объекта datetime с конкретной датой и временем
date_format = '%d.%m.%Y %H:%M'

# Парсинг строки в объект datetime
naive_datetime = datetime.strptime(EXPIRE_DATETIME, date_format)

# Указание временной зоны UTC+5
timezone = pytz.timezone('Etc/GMT-5')  # UTC+5

# Присвоение временной зоны к объекту datetime
EXPIRE_DATE = timezone.localize(naive_datetime)
