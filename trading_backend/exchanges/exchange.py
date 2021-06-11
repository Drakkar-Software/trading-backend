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
    def __init__(self, ccxt_exchange):
        self._ccxt_exchange = ccxt_exchange

    @classmethod
    def get_name(cls):
        return 'default'

    def get_authenticated_parameters(self, params) -> dict:
        return {}

    def get_orders_parameters(self, params) -> dict:
        return {}

    async def is_valid_account(self) -> (bool, str):
        return True, None
