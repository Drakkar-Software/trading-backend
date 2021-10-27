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


class Kucoin(exchanges.Exchange):
    SPOT_ID = (None, None)
    MARGIN_ID = (None, None)
    FUTURE_ID = (None, None)
    IS_SPONSORING = True
    HEADER_PART = "partner"
    HEADER_PART_ID = "id"
    HEADER_PART_SECRET = "secret"

    @classmethod
    def get_name(cls):
        return 'kucoin'

    def get_orders_parameters(self, params=None) -> dict:
        if self.HEADER_PART not in self._exchange.connector.client.options:
            self._exchange.connector.client.options[self.HEADER_PART] = {}
        options_broker = self._exchange.connector.client.options[self.HEADER_PART]
        if options_broker.get(self.HEADER_PART_ID, None) != self._get_id():
            self._exchange.connector.client.options[self.HEADER_PART][self.HEADER_PART_ID],\
                self._exchange.connector.client.options[self.HEADER_PART][self.HEADER_PART_SECRET] = self._get_id()
        return super().get_orders_parameters(params)

    async def _inner_is_valid_account(self) -> (bool, str):
        # Nothing to do
        return await super()._inner_is_valid_account()
