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
from datetime import datetime, date
from typing import List

import firefly as ff
from firefly_iaaa.domain.entity.role import Role
from firefly_iaaa.domain.entity.tenant import Tenant
from firefly_iaaa.domain.value_object.address import Address

# __pragma__('skip')
import bcrypt
import uuid
# __pragma__('noskip')


class User(ff.AggregateRoot):
    # OpenID standard fields
    sub: str = ff.id_(validators=[ff.HasLength(36)])
    name: str = ff.optional()
    given_name: str = ff.optional()
    family_name: str = ff.optional()
    middle_name: str = ff.optional()
    nickname: str = ff.optional()
    preferred_username: str = ff.optional(index=True)
    profile: str = ff.optional()
    picture: str = ff.optional()
    website: str = ff.optional()
    email: str = ff.optional(validators=[ff.IsValidEmail()], index=True)
    email_verified: bool = ff.optional(default=False)
    gender: str = ff.optional(validators=[ff.IsOneOf(('Male', 'Female'))])
    birthdate: date = ff.optional()
    zoneinfo: str = ff.optional()
    locale: str = ff.optional()
    phone_number: str = ff.optional()
    phone_number_verified: bool = ff.optional(default=False)
    address: Address = ff.optional()
    updated_at: datetime = ff.now()

    # Custom fields
    created_at: datetime = ff.now()
    deleted_at: datetime = ff.optional()
    password_hash: str = ff.optional(length=32)
    salt: str = ff.optional()
    roles: List[Role] = ff.list_()
    tenant: Tenant = ff.optional(index=True)

    # __pragma__('skip')
    @classmethod
    def create(cls, **kwargs):
        if 'email' in kwargs:
            kwargs['email'] = str(kwargs['email']).lower()
        try:
            kwargs['salt'] = bcrypt.gensalt()
            kwargs['password_hash'] = User._hash_password(kwargs['password'], kwargs['salt'])
        except KeyError:
            raise ff.MissingArgument('password is a required field for User::create()')
        return cls(**ff.build_argument_list(kwargs, cls))

    @classmethod
    def _hash_password(cls, password: str, salt: str):
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def correct_password(self, password: str):
        return self.password_hash == User._hash_password(password, self.salt)
    # __pragma__('noskip')
