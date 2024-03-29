#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.
from __future__ import annotations
from typing import List

import firefly as ff

from firefly_iaaa.domain.service.oauth_provider import OauthProvider
from firefly_iaaa.domain.entity.bearer_token import BearerToken

def test_revocation_response(auth_service: OauthProvider, bearer_messages_list: List[ff.Message], registry):

    VALID_METHOD_TYPES = ['GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'PATCH']
    token_status = ['active', 'expired', 'invalid']
    for i in range(6):
        method = VALID_METHOD_TYPES[i]
        # Check all http_methods except for POST don't invalidate token
        if method != 'POST':
            message = bearer_messages_list[i]['active']
            message.headers['http_method'] = method

            # Save token to reset to later
            old_token = message.token

            # Check token starts out valid
            token = registry(BearerToken).find(lambda x: x.access_token == message.access_token)
            assert_is_valid(token)
            message.token = message.access_token
            headers, body, status = auth_service.create_revocation_response(message)
            # Make sure token doesn't invalidate
            assert_is_valid(token)

            token = registry(BearerToken).find(lambda x: x.refresh_token == message.refresh_token)
            assert_is_valid(token)
            message.token = message.refresh_token
            # Make sure token doesn't invalidate
            headers, body, status = auth_service.create_revocation_response(message)
            assert_is_valid(token)

            # Reset to old token
            message.token = old_token

        
        for x in range(3):
            message = bearer_messages_list[i][token_status[x]]
            message.headers['http_method'] = 'POST'

            if i % 3 == 0:
                token = registry(BearerToken).find(lambda x: x.refresh_token == message.token)
            elif i % 3 == 1:
                token = registry(BearerToken).find(lambda x: x.access_token == message.token)
            else:
                continue
            
            # Check it starts off valid unless 'invalid' (expired should still have valid, vaaidation checks expiration differently)
            assert_is_valid(token, (x != 2))
            headers, body, status = auth_service.create_revocation_response(message)

            # Check access token always revoked
            # Check that it revokes refresh token if refresh is the provided token (i % 3 == 0) or already 'invalid'
            assert not token.is_valid == (i % 3 == 0 or (x == 2))
            assert not token.is_access_valid
            headers, body, status = auth_service.create_revocation_response(message)
            # Check that it's still revoked
            assert not token.is_valid == (i % 3 == 0 or (x == 2))
            assert not token.is_access_valid

def assert_is_valid(token: BearerToken, should_be: bool = True):
    assert token.is_valid == should_be
    assert token.is_access_valid == should_be

def test_revocation_response_missing_data(auth_service: OauthProvider, bearer_messages_second_list: List[ff.Message], registry):

    message = bearer_messages_second_list[-1]
    message.headers['http_method'] = 'POST'

    # Check for various missing attributes from message
    for i in range(16):
        message = bearer_messages_second_list[i]
        message.headers['http_method'] = 'POST'
        if i == 0:
            message.username = None
        if i == 1:
            message.password = None
        if i == 2:
            message.grant_type = None
        if i == 3:
            message.access_token = None
        if i == 4:
            message.client_id = None
        if i == 5:
            message.client_secret = None
        if i == 6:
            message.code = None
        if i == 7:
            message.code_challenge = None
        if i == 8:
            message.code_verifier = None
        if i == 9:
            message.redirect_uri = None
        if i == 10:
            message.refresh_token = None
        if i == 11:
            message.response_type = None
        if i == 12:
            message.scopes = None
        if i == 13:
            message.state = None
        if i == 14:
            message.token_type_hint = None
        if i == 15:
            message.client_secret = None
            message.password = None


        if i % 3 == 0:
            token = registry(BearerToken).find(lambda x: x.refresh_token == message.token)
        elif i % 3 == 1:
            token = registry(BearerToken).find(lambda x: x.access_token == message.token)
        else:
            continue
        
        # Check is valid at start
        assert_is_valid(token)
        headers, body, status = auth_service.create_revocation_response(message)
        # Check it revokes unless authentication fails (i == 15)
        # Check that it revokes refresh token if refresh is the provided token (i % 3 == 0)
        assert not token.is_valid == (i % 3 == 0 and i != 15)
        assert not token.is_access_valid == (i != 15)
        headers, body, status = auth_service.create_revocation_response(message) 
        # Check that it stays revoked
        assert not token.is_valid == (i % 3 == 0 and i != 15)
        assert not token.is_access_valid == (i != 15)
