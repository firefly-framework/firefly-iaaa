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

import pytest
import firefly_iaaa.domain as domain

from firefly_iaaa.domain.service.request_validator import OauthRequestValidators
from firefly_iaaa.domain.service.oauth_provider import OauthProvider
from firefly_iaaa.domain.entity.authorization_code import AuthorizationCode
from firefly_iaaa.domain.entity.bearer_token import BearerToken
from firefly_iaaa.domain.entity.user import User
from firefly_iaaa.domain.mock.mock_cache import MockCache


def set_kernel_user(registry, kernel, message):
    found_client = registry(domain.Client).find(lambda x: x.client_id == message.client_id)
    found_user = registry(domain.User).find(lambda x: (x.tenant_id == found_client.tenant_id) & (x.deleted_at.is_none()))
    kernel.user.id = found_user.sub