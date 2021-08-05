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
import ccxt.async_support
import trading_backend.exchanges as exchanges
import tests.util.create_order_tests as create_order_tests
from tests import ftx_exchange


def test_get_name(ftx_exchange):
    assert exchanges.FTX(ftx_exchange).get_name() == ccxt.async_support.ftx().name.lower()


@pytest.mark.asyncio
async def test_get_orders_parameters(ftx_exchange):
    exchange = exchanges.FTX(ftx_exchange)
    await create_order_tests.create_order_mocked_test(exchange,
                                                      exchange_private_post_order_method_name="privatePostOrders",
                                                      exchange_request_referral_key="externalReferralProgram",
                                                      should_contains=False)
