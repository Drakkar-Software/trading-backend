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
import trading_backend.exchanges as exchanges
from tests import gateio_exchange


def test_get_name(gateio_exchange):
    assert exchanges.GateIO(gateio_exchange).get_name() == ccxt.async_support.gateio().name.lower()


def test_get_orders_parameters(gateio_exchange):
    exchange = exchanges.GateIO(gateio_exchange)
    assert exchange.get_headers() == {exchange.HEADER_KEY: exchange._get_id()}
