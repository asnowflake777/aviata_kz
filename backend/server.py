import json

import aiohttp_cors
from aiohttp import web
from utils import get_from_redis

from consts import DIRECTIONS, DIRECTION_NAMES


routes = web.RouteTableDef()


@routes.get('/available_directions')
async def available_directions(request):
    print('new connection')
    response = []
    for fly_from_code, fly_to_code in DIRECTIONS:
        fly_from_name = DIRECTION_NAMES.get(fly_from_code)
        fly_to_name = DIRECTION_NAMES.get(fly_to_code)
        tmp = {
            'name': f'{fly_from_name}({fly_from_code}) - {fly_to_name}({fly_to_code})',
            'flyFrom': fly_from_code,
            'to': fly_to_code,
        }
        response.append(tmp)
    return web.json_response(response)


@routes.get('/mount_prices_for_direction')
async def get_mount_prices_for_direction(request):
    query = dict(request.query)
    key = f'{query.get("flyFrom")}-{query.get("to")}'
    flights = await get_from_redis(key)
    flights = json.loads(flights)
    return web.json_response(flights)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, host='127.0.0.1', port=5000)
