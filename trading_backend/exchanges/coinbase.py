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
import ccxt
import trading_backend.exchanges as exchanges
import trading_backend.enums


class Coinbase(exchanges.Exchange):
    # todo update this when coinbase broker id is available
    SPOT_ID = None
    MARGIN_ID = None
    FUTURE_ID = None
    REF_ID = None
    IS_SPONSORING = False

    @classmethod
    def get_name(cls):
        return 'coinbase'

    async def _ensure_broker_status(self):
        return f"Broker rebate is not enabled (missing broker id)."

    async def _get_api_key_rights(self) -> list[trading_backend.enums.APIKeyRights]:
        # warning might become deprecated
        # https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-users
        try:
            restrictions = (await self._exchange.connector.client.v2PrivateGetUserAuth())["data"]
            rights = []
            scopes = restrictions["scopes"]
            read_scopes = [
                "wallet:accounts:read",
                "wallet:buys:read",
                "wallet:sells:read",
                "wallet:orders:read",
                "wallet:trades:read",
                "wallet:user:read",
                "wallet:transactions:read",
            ]
            trade_scopes = [
                "wallet:buys:create",
                "wallet:sells:create",
            ]
            withdraw_scopes = [
                "wallet:withdrawals:create"
            ]
            if all(scope in scopes for scope in read_scopes):
                rights.append(trading_backend.enums.APIKeyRights.READING)
            if all(scope in scopes for scope in trade_scopes):
                rights.append(trading_backend.enums.APIKeyRights.SPOT_TRADING)
                rights.append(trading_backend.enums.APIKeyRights.MARGIN_TRADING)
                rights.append(trading_backend.enums.APIKeyRights.FUTURES_TRADING)
            if any(scope in scopes for scope in withdraw_scopes):
                rights.append(trading_backend.enums.APIKeyRights.WITHDRAWALS)
            return rights
        except ccxt.BaseError as err:
            self._exchange.logger.exception(
                err, True,
                f"Error when fetching {self.get_name()} api key rights: {err} ({err.__class__.__name__}). "
                f"This is not normal, endpoint might be deprecated, see"
                f"https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-users. "
                f"Using _get_api_key_rights_using_order() instead"
            )
            return await self._get_api_key_rights_using_order()

    async def _inner_is_valid_account(self) -> (bool, str):
        return False, await self._ensure_broker_status()
