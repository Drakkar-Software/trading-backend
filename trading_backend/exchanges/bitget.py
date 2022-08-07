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


class Bitget(exchanges.Exchange):
    SPOT_ID = "Octobot" + "#"    # include # as it is required to generate client_oid
    FUTURE_ID = "Octobot" + "#"    # include # as it is required to generate client_oid
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'bitget'

    def get_orders_parameters(self, params=None) -> dict:
        if "broker" not in self._exchange.connector.client.options:
            self._exchange.connector.client.options["broker"] = {}
        options_broker = self._exchange.connector.client.options["broker"]
        # same broker id for everything
        for broker_type in ("spot", "swap"):
            if options_broker.get(broker_type, None) != self._get_id():
                self._exchange.connector.client.options["broker"][broker_type] = self._get_id()
        return super().get_orders_parameters(params)

    async def _inner_is_valid_account(self) -> (bool, str):
        # Nothing to do
        return await super()._inner_is_valid_account()
