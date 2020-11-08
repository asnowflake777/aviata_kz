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
