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


class FTX(exchanges.Exchange):
    SPOT_ID = "Octobot"
    MARGIN_ID = "Octobot"
    FUTURE_ID = "Octobot"
    REF_ID = "33613187"
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'ftx'

    def get_orders_parameters(self, params=None) -> dict:
        params = super().get_orders_parameters(params)
        params.update({'externalReferralProgram': self._get_id()})
        return params

    async def _inner_is_valid_account(self) -> (bool, str):
        """
        Response doc from https://help.ftx.com/hc/en-us/articles/360044373831-External-Referral-Programs
        {
        'enabled': True,
        'externalReferralProgram': 'TradeX100',
        'readOnly': False,
        'requireWhitelistedIp': False,
        'subaccountNickname': None,
        'withdrawalEnabled': False
        }
        """
        # Seems to be unnecessary because the program name is overwritten in `get_orders_parameters`
        return await super()._inner_is_valid_account()
