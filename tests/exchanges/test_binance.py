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
from tests import binance_exchange


def test_get_name(binance_exchange):
    assert exchanges.Binance(binance_exchange).get_name() == ccxt.async_support.binance().name.lower()


def test_get_orders_parameters(binance_exchange):
    exchange = exchanges.Binance(binance_exchange)
    assert exchange.get_orders_parameters({"a": 1}) == {
        "a": 1,
        'newClientOrderId': exchange._order_custom_id
    }


@pytest.mark.asyncio
async def test_is_valid_account(binance_exchange):
    exchange = exchanges.Binance(binance_exchange)
    params = {"apiAgentCode": exchange._b_id}
    with pytest.raises(ccxt.AuthenticationError):
        await exchange.is_valid_account()
    with mock.patch.object(exchange._exchange.connector.client, "sapi_get_apireferral_ifnewuser",
                           mock.AsyncMock(return_value={"rebateWorking": False})) as sapi_get_apireferral_ifnewuser_mock:
        results = await exchange.is_valid_account()
        assert results[0] is False
        assert isinstance(results[1], str)
        sapi_get_apireferral_ifnewuser_mock.assert_called_once_with(params=params)
    with mock.patch.object(exchange._exchange.connector.client, "sapi_get_apireferral_ifnewuser",
                           mock.AsyncMock(return_value={"ifNewUser": False})) as sapi_get_apireferral_ifnewuser_mock:
        results = await exchange.is_valid_account()
        assert results[0] is False
        assert isinstance(results[1], str)
        sapi_get_apireferral_ifnewuser_mock.assert_called_once_with(params=params)
    with mock.patch.object(exchange._exchange.connector.client, "sapi_get_apireferral_ifnewuser",
                           mock.AsyncMock(return_value={})) as sapi_get_apireferral_ifnewuser_mock:
        results = await exchange.is_valid_account()
        assert results[0] is False
        assert isinstance(results[1], str)
        sapi_get_apireferral_ifnewuser_mock.assert_called_once_with(params=params)
    with mock.patch.object(exchange._exchange.connector.client, "sapi_get_apireferral_ifnewuser",
                           mock.AsyncMock(return_value={"rebateWorking": False, "ifNewUser": True})) \
            as sapi_get_apireferral_ifnewuser_mock:
        results = await exchange.is_valid_account()
        assert results[0] is False
        assert isinstance(results[1], str)
        sapi_get_apireferral_ifnewuser_mock.assert_called_once_with(params=params)
    with mock.patch.object(exchange._exchange.connector.client, "sapi_get_apireferral_ifnewuser",
                           mock.AsyncMock(return_value=None)) \
            as sapi_get_apireferral_ifnewuser_mock:
        results = await exchange.is_valid_account()
        assert results[0] is False
        assert isinstance(results[1], str)
        sapi_get_apireferral_ifnewuser_mock.assert_called_once_with(params=params)
    with mock.patch.object(exchange._exchange.connector.client, "sapi_get_apireferral_ifnewuser",
                           mock.AsyncMock(return_value={"rebateWorking": True, "ifNewUser": True})) \
            as sapi_get_apireferral_ifnewuser_mock:
        assert (await exchange.is_valid_account()) == (True, None)
        sapi_get_apireferral_ifnewuser_mock.assert_called_once_with(params=params)
