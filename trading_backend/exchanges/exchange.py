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
import ccxt

import trading_backend.errors


class Exchange:
    SPOT_ID = None
    MARGIN_ID = None
    FUTURE_ID = None
    IS_SPONSORING = False

    def __init__(self, exchange):
        self._exchange = exchange

    @classmethod
    def get_name(cls):
        return 'default'

    @classmethod
    def is_sponsoring(cls) -> bool:
        return cls.IS_SPONSORING

    def get_orders_parameters(self, params=None) -> dict:
        if params is None:
            params = {}
        return params

    async def is_valid_account(self) -> (bool, str):
        try:
            return await self._inner_is_valid_account()
        except ccxt.InvalidNonce as err:
            raise trading_backend.errors.TimeSyncError(err)
        except ccxt.ExchangeError as err:
            raise trading_backend.errors.ExchangeAuthError(err)

    async def _inner_is_valid_account(self) -> (bool, str):
        await self._exchange.connector.client.fetch_balance()
        return True, None

    def _get_id(self):
        if self._exchange.exchange_manager.is_future:
            return self.FUTURE_ID
        if self._exchange.exchange_manager.is_margin:
            return self.MARGIN_ID
        return self.SPOT_ID
