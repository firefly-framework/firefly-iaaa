from __future__ import annotations

import firefly as ff
import json

from firefly_iaaa import domain
from firefly_iaaa.application.api.generic_oauth_endpoint import GenericOauthEndpoint


@ff.rest(
    '/iaaa/token', method='POST', tags=['public']
)
class OauthTokenCreationService(GenericOauthEndpoint):
    _create_token: domain.CreateToken = None

    def __call__(self, **kwargs):
        headers, body = self._create_token(kwargs)
        return self._make_response(body, headers)