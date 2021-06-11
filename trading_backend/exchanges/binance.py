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
import trading_backend.exchanges as exchanges


class Binance(exchanges.Exchange):
    def __init__(self, ccxt_exchange):
        super().__init__(ccxt_exchange)
        self._order_custom_id = "x-bot"

    @classmethod
    def get_name(cls):
        return 'binance'

    def get_authenticated_parameters(self, params) -> dict:
        if params is None:
            params = {}
        params.update({'recvWindow': 60000})
        return params

    def get_orders_parameters(self, params) -> dict:
        if params is None:
            params = {}
        params.update({'newClientOrderId': self._order_custom_id})
        return params

    async def is_valid_account(self) -> (bool, str):
        details = await self._ccxt_exchange.private_get_apiReferral_ifNewUser()
        if not details.get("rebateWorking", False):
            return False, "This account has a referral code, which is incompatible"
        if not details.get("ifNewUser", False):
            return False, "This account is not new, which is incompatible"
        return True, None
