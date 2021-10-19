from __future__ import annotations

import firefly as ff
import json
from firefly_iaaa.application.service.generic_oauth_endpoint import GenericOauthEndpoint


@ff.rest(
    '/iaaa/introspect_token', method='POST', tags=['public']
)
class OauthTokenIntrospectionService(GenericOauthEndpoint):

    def __call__(self, **kwargs):
        message = self._make_message(kwargs)

        headers, body, status =  self._oauth_provider.create_introspect_response(message)
        # if status == 200:
        #     body = json.loads(body)
        # #? Add headers?

        return json.loads(body)

    def _make_message(self, incoming_kwargs: dict):
        headers = self._add_method_to_headers(incoming_kwargs)
        message_body = {
            'headers': headers,
            'client_id': self._get_client_id(incoming_kwargs.get('client_id')),
            'state': incoming_kwargs.get('state'),
            'token': incoming_kwargs.get('token')
        }

        if incoming_kwargs.get('username'):
            message_body['username'] = incoming_kwargs.get('username') 
        if incoming_kwargs.get('password'):
            message_body['password'] = incoming_kwargs.get('password') 
        if incoming_kwargs.get('client_secret'):
            message_body['client_secret'] = incoming_kwargs.get('client_secret') 
        if not message_body['token']:
            if incoming_kwargs.get('access_token'):
                message_body['token'] = incoming_kwargs.get('access_token') 
        if not message_body['token']:
            if incoming_kwargs.get('refresh_token'):
                message_body['token'] = incoming_kwargs.get('refresh_token')
        if incoming_kwargs.get('token_type_hint'):
            message_body['token_type_hint'] = incoming_kwargs.get('token_type_hint')

        return self._message_factory.query(
            name='OauthIntrospectTokenMessage',
            data=message_body
        )