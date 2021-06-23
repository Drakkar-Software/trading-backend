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


class Exchange:
    SPOT_ID = None
    MARGIN_ID = None
    FUTURE_ID = None

    def __init__(self, exchange):
        self._exchange = exchange

    @classmethod
    def get_name(cls):
        return 'default'

    def get_orders_parameters(self, params=None) -> dict:
        if params is None:
            params = {}
        return params

    async def is_valid_account(self) -> (bool, str):
        return True, None

    def _get_id(self):
        if self._exchange.exchange_manager.is_future:
            return self.FUTURE_ID
        if self._exchange.exchange_manager.is_margin:
            return self.MARGIN_ID
        return self.SPOT_ID
