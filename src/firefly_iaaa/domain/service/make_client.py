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
import uuid
import firefly_iaaa.domain as domain


END_USER_CLIENT = {

}

class MakeUser(ff.DomainService):
    _registry: ff.Registry = None

    def __call__(self, username: str, password: str, tenant_name: str, grant_type: str, scopes: List = [], **kwargs):
        tenant = domain.Tenant(
            name=tenant_name
        )
        user = domain.User.create(
            email=username,
            password=password,
            tenant=tenant,
            **kwargs
        )

        # if authorization:
        #     if pkce:
            
        #     else:
        
        # if implicit:

        # if resource_owner:

        # if client_credentials:

        # generic_client_data = { #same as end user
        #     'client_id': user.sub,
        #     'name': username,
        #     'tenant': tenant,
        #     'grant_type': grant_type,
        #     'scopes': scopes,
        # }

        # auth_code_client_data = {
        #     'default_redirect_uri': kwargs['default_redirect_uri'],
        #     'redirect_uris': kwargs['redirect_uris'],
        #     'allowed_response_types': 'code',
        # }

        # auth_code_w_pkce_client_data = {
        #     'uses_pkce': True,
        # }

        # client_secret_client_data =  {
        #     'client_secret': str(uuid.uuid4()),
        # }

        # implicit_client_data = {
        #     'default_redirect_uri': kwargs['default_redirect_uri'],
        #     'redirect_uris': kwargs['redirect_uris'],
        #     'allowed_response_types': 'token',
        # }




        client = domain.Client.create(
            client_id=user.sub,
            tenant=tenant,
            name=username,
            grant_type=grant_type,
            scopes=scopes,
            client_secret=uuid.uuid4(),
            **kwargs
        )

        role = self._registry(domain.Role).find('fad2cf43-01df-44a1-bef4-0446d066e0bc')
        user.add_role(role)

        # Append at end to avoid appending before an error during entity creation
        self._registry(domain.Tenant).append(tenant)
        self._registry(domain.User).append(user)
        self._registry(domain.Client).append(client)


    def make_auth(self, x):
        pass

    def make_auth_with_pkce(self, x):
        pass

    def make_auth_with_pkce(self, x):
        pass

    def make_auth_with_pkce(self, x):
        pass