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
import trading_backend.enums
import trading_backend
from tests import coinbase_exchange


def test_get_name(coinbase_exchange):
    assert exchanges.Coinbase(coinbase_exchange).get_name() == ccxt.async_support.coinbase().id.lower()


@pytest.mark.asyncio
async def test_get_orders_parameters(coinbase_exchange):
    exchange = exchanges.Coinbase(coinbase_exchange)
    assert exchange.get_orders_parameters({}) == {}


@pytest.mark.asyncio
async def test_inner_is_valid_account(coinbase_exchange):
    exchange = exchanges.Coinbase(coinbase_exchange)
    assert await exchange._inner_is_valid_account() == (False, await exchange._ensure_broker_status())


@pytest.mark.asyncio
async def test_get_api_key_rights(coinbase_exchange):
    exchange = exchanges.Coinbase(coinbase_exchange)
    with mock.patch.object(
        exchange._exchange.connector.client, "v2PrivateGetUserAuth",
        mock.AsyncMock(return_value={"data": {"scopes": [
            "wallet:accounts:read",
            "wallet:buys:read",
            "wallet:sells:read",
            "wallet:orders:read",
            "wallet:trades:read",
            "wallet:user:read",
            "wallet:transactions:read",
            "wallet:buys:create",
        ]}})
    ) as v2PrivateGetUserAuth_mock:
        assert await exchange._get_api_key_rights() == [
            trading_backend.enums.APIKeyRights.READING
        ]
        v2PrivateGetUserAuth_mock.assert_awaited_once()
    with mock.patch.object(
        exchange._exchange.connector.client, "v2PrivateGetUserAuth",
        mock.AsyncMock(return_value={"data": {"scopes": [
            "wallet:accounts:read",
            "wallet:buys:read",
            "wallet:sells:read",
            "wallet:orders:read",
            "wallet:trades:read",
            "wallet:user:read",
            "wallet:transactions:read",
            "wallet:buys:create",
            "wallet:sells:create",
            "wallet:withdrawals:create",
        ]}})
    ) as v2PrivateGetUserAuth_mock:
        assert await exchange._get_api_key_rights() == [
            trading_backend.enums.APIKeyRights.READING,
            trading_backend.enums.APIKeyRights.SPOT_TRADING,
            trading_backend.enums.APIKeyRights.MARGIN_TRADING,
            trading_backend.enums.APIKeyRights.FUTURES_TRADING,
            trading_backend.enums.APIKeyRights.WITHDRAWALS
        ]
        v2PrivateGetUserAuth_mock.assert_awaited_once()
