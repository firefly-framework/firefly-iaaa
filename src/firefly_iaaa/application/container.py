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
import base64

import firefly as ff

import firefly_di as di
import firefly_iaaa.domain as domain

from firefly_aws import infrastructure as aws_infra
from firefly_iaaa.domain.mock.mock_cache import MockCache
from dotenv import load_dotenv


load_dotenv()
class Container(di.Container):
    cache: ff.Cache = MockCache if \
        os.environ.get('FF_ENVIRONMENT') == 'test' else aws_infra.DdbCache
    oauthlib_request_validator: domain.OauthRequestValidators = domain.OauthRequestValidators
    request_validator: domain.OauthProvider = domain.OauthProvider
    message_factory: ff.MessageFactory = ff.MessageFactory
    debugging_print_one: str = lambda x: print('WE HAVE AN OS ENVIRONMENT', os.environ)
    debugging_print_two: str = lambda x: print('WE HAVE AN OS ENVIRONMENT', os.environ.__dict__)
    secret_key: str = lambda x: str(base64.b64decode(os.environ['PEM']), "utf-8")
    subdomain: str = lambda x: 'staging-connected-sports'