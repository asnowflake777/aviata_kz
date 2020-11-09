import asyncio
import json
import pytz
from copy import deepcopy
from time import sleep
from calendar import Calendar
from collections import defaultdict

import aiohttp
from datetime import datetime

import schedule as schedule
from dateutil.relativedelta import relativedelta

import consts
from errors import GettingFlightsInfoError
from utils import put_to_redis


def get_calendar(
        date_start: datetime.date,
        date_stop: datetime.date
):
    my_calendar = Calendar(0)
    first_year = date_start.year
    last_year = date_stop.year
    first_month = date_start.month
    last_month = date_stop.month

    months_diff = (last_year - first_year) * 12 + (last_month - first_month)

    calendar = defaultdict()
    month = first_month
    year = first_year
    for _ in range(months_diff + 1):
        calendar[f'{month}/{year}'] = {date.strftime('%m/%d'): {} for date in my_calendar.itermonthdates(year, month)}
        month += 1

        if month > 12:
            year += 1
            month = 1

    while True:
        yield deepcopy(calendar)


def get_query_params(
        date_from: datetime.date,
        date_to: datetime.date,
):
    date_from_str = date_from.strftime(consts.REQUEST_DATE_FMT)
    date_to_str = date_to.strftime(consts.REQUEST_DATE_FMT)

    for fly_from, fly_to in consts.DIRECTIONS:
        query_name = f'{fly_from}-{fly_to}'
        query_params = {
            'flyFrom': fly_from,
            'to': fly_to,
            'dateFrom': date_from_str,
            'dateTo': date_to_str,
            'partner': consts.PARTNER,
            'v': consts.API_VERSION,
        }
        yield query_name, query_params


async def get_task_args():
    date_start = datetime.now().date()
    date_stop = date_start + relativedelta(months=1)

    calendar_gen = get_calendar(date_start, date_stop)
    query_params_gen = get_query_params(date_start, date_stop)

    for calendar, (query_name, query_params) in zip(calendar_gen, query_params_gen):
        yield date_start, date_stop, calendar, query_name, query_params


async def get_n_put_flight_info_in_redis(
        session: aiohttp.ClientSession,
        url: str,
        task_args: tuple,
) -> None:
    date_start, date_stop, calendar, query_name, query_params = task_args
    async with session.get(url, params=query_params) as response:
        response_json = await response.json()

        if response.status != 200:
            raise GettingFlightsInfoError

        data = response_json.get('data')
        currency = response_json.get('currency')
        lowest_price_data = None
        for flight in data:
            departure = flight.get('aTimeUTC')
            booking_token = flight.get('booking_token')
            price = flight.get('price')

            if not all([departure, booking_token, price]):
                continue

            departure = datetime.fromtimestamp(departure, tz=pytz.UTC)
            full_date_in_str = departure.strftime(consts.REQUEST_DATE_FMT)
            day, year_n_month = full_date_in_str.split('/', maxsplit=1)
            flight_at_same_date = calendar[year_n_month].get(full_date_in_str)

            if (not flight_at_same_date) or (flight_at_same_date['price'] < price):
                flight_info = {
                    'price': price,
                    'lowest_price': False,
                    'booking_token': booking_token,
                }

                calendar[year_n_month][full_date_in_str] = flight_info

            if (not lowest_price_data) or lowest_price_data['price'] < price:
                lowest_price_data = {'date': [full_date_in_str], 'price': price}
            elif lowest_price_data and lowest_price_data['price'] == price:
                lowest_price_data['date'].append(full_date_in_str)

        if lowest_price_data:
            for date in lowest_price_data['date']:
                lowest_price_day, lowest_price_year_n_month = date.split('/', maxsplit=1)
                calendar[lowest_price_year_n_month][date]['lowest_price'] = True
                print(lowest_price_data)

        result = []
        for month_year, days in calendar.items():
            month, year = month_year.split('/')
            tmp = {
                'sheet_name': f'{consts.MONTH_NAMES[month]} {year}',
                'days': [{'day': date.split('/')[0], 'flight_data': flight_data} for date, flight_data in days.items()]
            }
            result.append(tmp)
        print(result[0])
        await put_to_redis(query_name, json.dumps({'currency': currency, 'calendar': result}))


async def main():
    print('Downloading started')
    tasks = []
    url = consts.SKY_PICKER_URL + consts.FLIGHTS_SEARCH_ENDPOINT
    async with aiohttp.ClientSession() as session:
        async for task_args in get_task_args():
            task = asyncio.create_task(get_n_put_flight_info_in_redis(session, url, task_args))
            tasks.append(task)
        await asyncio.gather(*tasks)
    print('Downloading finished')


def runner():
    for i in range(1, 6):
        try:
            asyncio.run(main())
            break
        except GettingFlightsInfoError as err:
            print('got error', err.args)
            sleep(i)


if __name__ == '__main__':
    schedule.every().day.at("06:22").do(runner)

    while True:
        try:
            schedule.run_pending()
            sleep(5)
        except KeyboardInterrupt:
            break

    print('\nBay!\n')
