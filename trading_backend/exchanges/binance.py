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


class Binance(exchanges.Exchange):
    SPOT_ID = "T9698EB7"
    MARGIN_ID = None
    FUTURE_ID = "uquVg2pc"
    REF_ID = "135007948"
    IS_SPONSORING = True

    @classmethod
    def get_name(cls):
        return 'binance'

    def _get_order_custom_id(self):
        return f"x-{self._get_id()}{self._exchange.connector.client.uuid22()}"

    def get_orders_parameters(self, params=None) -> dict:
        params = super().get_orders_parameters(params)
        params.update({'newClientOrderId': self._get_order_custom_id()})
        return params

    async def _inner_is_valid_account(self) -> (bool, str):
        try:
            details = await self._exchange.connector.client.sapi_get_apireferral_ifnewuser(
                params=self._exchange._get_params({
                    "apiAgentCode": self._get_id()
                })
            )
            if not details.get("rebateWorking", False):
                return False, f"This account has a referral id and it is not {self.REF_ID}, " \
                              f"which is incompatible ({self.REF_ID} or no referral id is required)"
            if not details.get("ifNewUser", False):
                return False, "This account is not new, which is incompatible"
        except AttributeError:
            return False, "Invalid request parameters"
        return True, None
