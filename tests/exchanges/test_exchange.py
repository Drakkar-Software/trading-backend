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
import trading_backend.exchanges as exchanges
from tests import default_exchange


def test_get_name(default_exchange):
    assert exchanges.Exchange(default_exchange).get_name() == exchanges.Exchange.get_name()


def test_get_orders_parameters(default_exchange):
    assert exchanges.Exchange(default_exchange).get_orders_parameters({"a": 1}) == {"a": 1}


@pytest.mark.asyncio
async def test_is_valid_account(default_exchange):
    assert await exchanges.Exchange(default_exchange).is_valid_account() == (True, None)
