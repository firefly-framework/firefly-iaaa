from __future__ import annotations
from typing import List

import firefly as ff
import json
from .conftest import set_kernel_user

async def test_create_token_code_from_auth_endpoint(client, registry, bearer_messages: List[ff.Message], kernel):

    data = {
            'state': bearer_messages[0]['active'].state,
            'username': bearer_messages[0]['active'].username,
    }
    set_kernel_user(registry, kernel, bearer_messages[0]['active'])

    first_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await first_response.text())['data']
    assert 'error' in resp

    data['grant_type'] = bearer_messages[0]['active'].grant_type
    second_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await second_response.text())['data']
    assert 'error' in resp

    data['client_id'] = bearer_messages[0]['active'].client_id
    third_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await third_response.text())['data']
    assert 'error' in resp

    data['password'] = bearer_messages[0]['active'].password
    fourth_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await fourth_response.text())['data']
    assert 'error' in resp

    data['code'] = bearer_messages[0]['active'].code
    fifth_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await fifth_response.text())['data']
    assert 'error' in resp

    data['code_verifier'] = bearer_messages[0]['active'].code_verifier
    final_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    assert final_response.status == 200
    resp = json.loads(await final_response.text())['data']
    assert resp['access_token'] is not None
    assert resp['refresh_token'] is not None
    assert resp['expires_in'] == 3600

    final_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await final_response.text())['data']
    assert 'error' in resp

async def test_create_token_code_from_refresh_endpoint(client, kernel, registry, bearer_messages: List[ff.Message]):

    data = {
            'state': bearer_messages[1]['active'].state,
            'username': bearer_messages[1]['active'].username,
    }
    set_kernel_user(registry, kernel, bearer_messages[0]['active'])
    
    first_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await first_response.text())['data']
    assert 'error' in resp

    data['grant_type'] = bearer_messages[1]['active'].grant_type
    second_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await second_response.text())['data']
    assert 'error' in resp

    data['client_id'] = bearer_messages[1]['active'].client_id
    third_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await third_response.text())['data']
    assert 'error' in resp

    data['password'] = bearer_messages[1]['active'].password
    fourth_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await fourth_response.text())['data']
    assert 'error' in resp

    data['refresh_token'] = bearer_messages[1]['active'].refresh_token
    final_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    assert final_response.status == 200
    resp = json.loads(await final_response.text())['data']
    assert resp['access_token'] is not None
    assert resp['refresh_token'] is not None
    assert resp['expires_in'] == 3600

    final_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await final_response.text())['data']
    assert 'error' in resp

async def test_create_token_code_from_client_credentials_endpoint(client, kernel, registry, bearer_messages: List[ff.Message]):

    data = {
            'state': bearer_messages[3]['active'].state,
    }
    set_kernel_user(registry, kernel, bearer_messages[0]['active'])
    
    first_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await first_response.text())['data']
    assert 'error' in resp

    data['grant_type'] = bearer_messages[3]['active'].grant_type
    second_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await second_response.text())['data']
    assert 'error' in resp

    data['client_id'] = bearer_messages[3]['active'].client_id
    third_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    resp = json.loads(await third_response.text())['data']
    assert 'error' in resp

    data['client_secret'] = bearer_messages[3]['active'].client_secret
    final_response = await client.post('/firefly-iaaa/iaaa/token', data=json.dumps(data), headers={'Referer': 'abc'})
    assert final_response.status == 200
    resp = json.loads(await final_response.text())['data']
    assert resp['access_token'] is not None
    assert 'refresh_token' not in resp
    assert resp['expires_in'] == 3600
