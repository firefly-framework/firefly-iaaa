from __future__ import annotations
from typing import List

import firefly as ff
import json

async def test_oauth_login_endpoint(client, registry, bearer_messages: List[ff.Message], kernel, context_map):
    data = {
            'state': bearer_messages[2]['active'].state,
            'username': bearer_messages[2]['active'].username,
    }

    first_response = await client.post('/firefly-iaaa/iaaa/login', data=json.dumps(data), headers={'Referer': 'abc'})
    assert first_response.status == 200
    first_response = json.loads(await first_response.text())
    assert first_response['message'] == 'error'

    data['grant_type'] = bearer_messages[2]['active'].grant_type
    second_response = await client.post('/firefly-iaaa/iaaa/login', data=json.dumps(data), headers={'Referer': 'abc'})
    assert second_response.status == 200
    second_response = json.loads(await second_response.text())
    assert second_response['message'] == 'error'

    data['client_id'] = bearer_messages[2]['active'].email
    third_response = await client.post('/firefly-iaaa/iaaa/login', data=json.dumps(data), headers={'Referer': 'abc'})
    assert third_response.status == 200
    third_response = json.loads(await third_response.text())
    assert third_response['message'] == 'error'

    data['password'] = bearer_messages[2]['active'].password
    fourth_response = await client.post('/firefly-iaaa/iaaa/login', data=json.dumps(data), headers={'Referer': 'abc'})
    assert fourth_response.status == 200
    resp = json.loads(await fourth_response.text())
    assert resp['message'] == 'success'
    assert resp['data']['access_token'] is not None
    assert resp['data']['refresh_token'] is not None


    data['password'] = 'wrong password'
    fifth_response = await client.post('/firefly-iaaa/iaaa/login', data=json.dumps(data), headers={'Referer': 'abc'})
    assert fifth_response.status == 403
