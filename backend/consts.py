SKY_PICKER_URL = 'https://api.skypicker.com'

FLIGHTS_SEARCH_ENDPOINT = '/flights'

API_VERSION = '3'

PARTNER = 'picky'

DIRECTIONS = [
    ('ALA', 'TSE'),
    ('TSE', 'ALA'),
    ('ALA', 'MOW'),
    ('MOW', 'ALA'),
    ('ALA', 'CIT'),
    ('CIT', 'ALA'),
    ('TSE', 'MOW'),
    ('MOW', 'TSE'),
    ('TSE', 'LED'),
    ('LED', 'TSE')
]

DIRECTION_NAMES = {
    'ALA': 'Алматы',
    'TSE': 'Астана',
    'MOW': 'Москва',
    'LED': 'С-Петербург',
    'CIT': 'Шымкент'
}


REQUEST_DATE_FMT = '%d/%m/%Y'

REDIS_URL = 'redis://localhost:6379'


MONTH_NAMES = {
    '1': 'Январь',
    '2': 'Февраль',
    '3': 'Март',
    '4': 'Апрель',
    '5': 'Май',
    '6': 'Июнь',
    '7': 'Июль',
    '8': 'Август',
    '9': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь',
}
