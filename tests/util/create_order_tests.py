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
import mock
import trading_backend.exchanges as exchanges


async def create_order_mocked_test(exchange: exchanges.Exchange,
                                   exchange_private_post_order_method_name: str,
                                   exchange_request_referral_key: str,
                                   should_contains: bool = True,
                                   symbol: str = "BTC/USDT",
                                   amount: int = 1,
                                   price: int = 1):
    with mock.patch.object(exchange._exchange.connector.client,
                           exchange_private_post_order_method_name,
                           mock.AsyncMock(return_value={})) as post_order_mock:
        # without referral patch
        await exchange._exchange.connector.client.create_limit_buy_order(symbol, amount, price)
        if should_contains:
            assert exchange._get_id() not in post_order_mock.call_args[0][0].get(exchange_request_referral_key, "")
        else:
            assert exchange._get_id() != post_order_mock.call_args[0][0].get(exchange_request_referral_key, "")

        # with referral patch
        await exchange._exchange.connector.client.create_limit_buy_order(symbol, amount, price,
                                                                         params=exchange.get_orders_parameters())
        if should_contains:
            assert exchange._get_id() in post_order_mock.call_args[0][0].get(exchange_request_referral_key, "")
        else:
            assert exchange._get_id() == post_order_mock.call_args[0][0].get(exchange_request_referral_key, "")
