from __future__ import annotations

import firefly as ff
import firefly_iaaa.domain as domain
from firefly_iaaa.application.service.generic_oauth_endpoint import GenericOauthEndpoint


@ff.rest(
    '/iaaa/revoke-token', method='POST', tags=['public']
)
class OauthTokenRevocationService(GenericOauthEndpoint):
    _oauth_provider: domain.OauthProvider = None
    _kernel: ff.Kernel = None
    _message_factory: ff.MessageFactory = None

    def __call__(self, **kwargs):
        message = self._make_message(kwargs)

        headers, body, status =  self._oauth_provider.create_revocation_response(message)
        # if status == 200:
        #     body = json.loads(body)
        # #? Add headers?

        return body

    def _make_message(self, incoming_kwargs: dict):
        headers = self._add_method_to_headers(incoming_kwargs)
        message_body = {
            'headers': headers,
            'token': incoming_kwargs.get('token'),
            "client_id": self._get_client_id(incoming_kwargs.get('client_id')),
            "state": incoming_kwargs.get('state')
        }

        if incoming_kwargs.get('username'):
            message_body['username'] = incoming_kwargs.get('username') 
        if incoming_kwargs.get('password'):
            message_body['password'] = incoming_kwargs.get('password') 
        if incoming_kwargs.get('client_secret'):
            message_body['client_secret'] = incoming_kwargs.get('client_secret')


        return self._message_factory.query(
            name='OauthRevokeTokenMessage',
            data=message_body
        )
