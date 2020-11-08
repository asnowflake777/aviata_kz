import asyncio
import json
from time import sleep

import aiohttp
from datetime import datetime

import schedule as schedule
from dateutil.relativedelta import relativedelta

import consts
from utils import put_to_redis


async def get_query_params():
    date_from = datetime.now().date()
    date_to = date_from + relativedelta(months=1)
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


async def get_n_put_flight_info_in_redis(
        session: aiohttp.ClientSession,
        url: str,
        query_params: dict,
        redis_key: str
) -> None:
    async with session.get(url, params=query_params) as response:
        response_json = await response.json()
        flights = []
        currency = response_json['currency']
        data = response_json['data']
        for flight in data:
            departure = flight.get('aTimeUTC')
            booking_token = flight.get('booking_token')
            price = flight.get('price')

            if all([departure, booking_token, currency, price]):
                flights.append({
                    'departure': departure,
                    'booking_token': booking_token,
                    'currency': currency,
                    'price': price
                })

        await put_to_redis(redis_key, json.dumps(flights))


async def main():
    print('Downloading started')
    tasks = []
    url = consts.SKY_PICKER_URL + consts.FLIGHTS_SEARCH_ENDPOINT
    async with aiohttp.ClientSession() as session:
        async for query_name, query_params in get_query_params():
            task = asyncio.create_task(get_n_put_flight_info_in_redis(session, url, query_params, query_name))
            tasks.append(task)
        await asyncio.gather(*tasks)
    print('Downloading finished')


def runner():
    asyncio.run(main())


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(runner)

    while True:
        try:
            schedule.run_pending()
            sleep(5)
        except KeyboardInterrupt:
            break

    print('\nBay!\n')
