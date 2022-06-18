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
import ccxt.async_support
import pytest
import mock

import trading_backend.exchanges as exchanges
import tests.util.create_order_tests as create_order_tests
from tests import bybit_exchange


def test_get_name(bybit_exchange):
    assert exchanges.Bybit(bybit_exchange).get_name() == ccxt.async_support.bybit().id.lower()


@pytest.mark.asyncio
async def test_spot_orders_parameters(bybit_exchange):
    exchange = exchanges.Bybit(bybit_exchange)
    await exchange._exchange.connector.client.load_markets()
    exchange._exchange.connector.client.market("BTC/USDT:USDT")['spot'] = True
    with mock.patch.object(exchange._exchange.connector.client,
                           "fetch", mock.AsyncMock(return_value=[])):
        await create_order_tests.create_order_mocked_test_args(
            exchange,
            exchange_private_post_order_method_name="privatePostSpotV1Order",
            exchange_request_referral_key="agentSource",
            should_contains=False)


@pytest.mark.asyncio
async def test_future_orders_parameters(bybit_exchange):
    bybit_exchange.exchange_manager.is_future = True
    exchange = exchanges.Bybit(bybit_exchange)
    await exchange._exchange.connector.client.load_markets()
    with mock.patch.object(exchange._exchange.connector.client,
                           "fetch", mock.AsyncMock(return_value=[])):
        await create_order_tests.create_order_mocked_test_args(
            exchange,
            exchange_private_post_order_method_name="privatePostPrivateLinearOrderCreate",
            exchange_request_referral_key="Referer",
            should_contains=False)
