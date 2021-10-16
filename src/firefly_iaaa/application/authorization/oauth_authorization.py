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

import firefly as ff
import firefly_iaaa.infrastructure as infra


class AuthorizeRequest(ff.Handler, ff.LoggerAware):
    _kernel: ff.Kernel = None
    _oauth_provider: infra.OauthProvider = None

    def handle(self, message: ff.Message):
        # Should have scopes and access_token on message
        if not message.access_token:
            token = self._get_token()
            if not token:
                return False
            message.access_token = token
        if not message.scopes:
            message.scopes = self._kernel.user.scopes

        validated, resp = self._oauth_provider.verify_request(message)
        #! requested resource/resource owner
        #compare to user on resp
        return validated

    def _get_token(self):
        token = None
        for k, v in self._kernel.http_request['headers'].items():
            if k.lower() == 'authorization':
                if not v.lower().startswith('bearer'):
                    raise ff.UnauthenticatedError()
                token = v.split(' ')[-1]
        return token