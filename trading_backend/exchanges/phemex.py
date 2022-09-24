#  Drakkar-Software trading-backend
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import aiohttp.streams

import trading_backend.exchanges as exchanges


class Phemex(exchanges.Exchange):
    SPOT_ID = "Octobot"
    MARGIN_ID = None
    FUTURE_ID = "Octobot"
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'phemex'

    def _get_order_custom_id(self):
        return f"{self._get_id()}{self._exchange.connector.client.uuid16()}"

    def get_orders_parameters(self, params=None) -> dict:
        params = super().get_orders_parameters(params)
        params.update({'clOrdID': self._get_order_custom_id()})
        return params
