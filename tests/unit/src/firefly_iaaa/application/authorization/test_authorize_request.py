from __future__ import annotations
from typing import List

import pytest
import firefly as ff
import json
import firefly_iaaa.domain as domain
import firefly_iaaa.application as application

async def test_authorize_request(bearer_messages_list: List[ff.Message], message_factory, sut, kernel):
    kernel.user.id = bearer_messages_list[0]['active'].client_id
    data = {
            'headers': bearer_messages_list[0]['active'].headers,
            'state': bearer_messages_list[0]['active'].state,
            'username': bearer_messages_list[0]['active'].username,
            'password': bearer_messages_list[0]['active'].password,
    }

    message = message_factory.query(
        name='a1b2c3',
        data=data,
    )
    validated = sut.handle(message)
    assert not validated

    data['access_token'] = bearer_messages_list[0]['active'].access_token
    message = message_factory.query(
        name='a1b2c3',
        data=data,
    )
    validated = sut.handle(message)
    assert validated



@pytest.fixture()
def sut(container):
    cont = container.build(application.AuthorizeRequest)
    return cont