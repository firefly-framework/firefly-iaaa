from __future__ import annotations
from typing import List

from oauthlib.common import Request

from firefly_iaaa.domain.service.request_validator import OauthRequestValidators



def test_get_default_scopes(validator: OauthRequestValidators, oauth_request_list: List[Request]):
    for i in range(4):

        # Check default scopes for request
        assert validator.get_default_scopes('', oauth_request_list[i]) == ['fake-scopes', f'faker-scope{i}'], 'Tests client existing on request'

