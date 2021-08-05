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
import pytest
import mock
import ccxt.async_support
import trading_backend.exchanges as exchanges
import trading_backend
from tests import okex_exchange


def test_get_name(okex_exchange):
    assert exchanges.OKEx(okex_exchange).get_name() == ccxt.async_support.okex().name.lower()


@pytest.mark.asyncio
async def test_get_orders_parameters(okex_exchange):
    exchange = exchanges.OKEx(okex_exchange)
    with mock.patch.object(exchange._exchange.connector.client,
                           "privatePostTradeOrder",
                           mock.AsyncMock(return_value={})) as privatePostTradeOrder_mock:

        # without broker id patch
        await exchange._exchange.connector.client.create_limit_buy_order("BTC/USDT", 1, 1)
        assert exchange._get_id() not in privatePostTradeOrder_mock.call_args[0][0].get("clOrdId", "")

        # with broker id patch
        exchange.get_orders_parameters()
        await exchange._exchange.connector.client.create_limit_buy_order("BTC/USDT", 1, 1)
        assert exchange._get_id() in privatePostTradeOrder_mock.call_args[0][0].get("clOrdId", "")
