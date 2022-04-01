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
import os
from typing import List

import firefly as ff
import firefly_iaaa.domain as domain


class RemoveUser(ff.DomainService, ff.LoggerAware):
    _registry: ff.Registry = None
    _user_deleted_event = os.environ.get('USER_DELETED_EVENT') or 'iaaa.DeleteUser'

    def __call__(self, user_id: str, **kwargs):
        user: domain.User = self._registry(domain.User).find(lambda x: (x.sub == user_id) & (x.deleted_at.is_none()))
        if user:
            self.info(f'Found user {user.sub}. Deleting...')
            user.salt = None
            user.password_hash = None
            user.roles = []
            self.invoke(self._user_deleted_event, {'sub': user.sub})

            print('Deleting Creds')
            for credentials in (domain.BearerToken, domain.AuthorizationCode):
                print('running cred', credentials)
                found_creds = self._registry(credentials).filter(lambda c: c.user.sub == user_id)
                print(f'found {len(found_creds)} creds')
                for cred in found_creds:
                    print('cred', cred)
                    cred.invalidate()
                    print('cred', cred)
                    self._registry(credentials).remove(cred)
                    print('cred', cred)

            # bearer_tokens: List[domain.BearerToken] = self._registry(domain.BearerToken).filter(lambda bt: bt.user.sub == user.sub)
            # for bt in bearer_tokens:
            #     bt.invalidate()
            #     self._registry(domain.BearerToken).remove(bt)

            # auth_codes: List[domain.AuthorizationCode] = self._registry(domain.AuthorizationCode).filter(lambda ac: ac.user.sub == user.sub)
            # for ac in auth_codes:
            #     ac.invalidate()
            #     self._registry(domain.AuthorizationCode).remove(ac)
            return {'status': 'success', 'message': 'User deleted'}
        return {'status': 'error', 'message': 'No user found'}
