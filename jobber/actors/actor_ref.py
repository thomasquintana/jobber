# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Thomas Quintana <quintana.thomas@gmail.com>

from urlparse import urlparse

from jobber.constants import JOBBER_CTX_HOSTNAME, JOBBER_CTX_PORT, \
                             JOBBER_PORT, JOBBER_SCHEME
from jobber.errors import ACTOR_REF_INVALID_PATH, ACTOR_REF_INVALID_SCHEME

class ActorRef(object):
  '''
  
  Positional Arguments:
  context -- A dictionary container holding the context state.
  path    -- A valid url path to the referenced actor.
  '''

  def __init__(self, actor, context, path):
    super(ActorRef, self).__init__()
    self._actor = actor
    self._context = context
    self._path = self._validate(context, urlparse(path))

  def _validate(self, context, path):
    if len(path.path) == 0:
      raise ValueError(ACTOR_REF_INVALID_PATH)
    if not path.scheme == JOBBER_SCHEME:
      raise ValueError(ACTOR_REF_INVALID_SCHEME)
    path_tokens = ["%s://" % JOBBER_SCHEME]
    if path.hostname is not None:
      path_tokens.append(path.hostname)
    else:
      path_tokens.append(context.get(JOBBER_CTX_HOSTNAME, "localhost"))
    path_tokens.append(":")
    if path.port is not None:
      path_tokens.append(str(path.port))
    else:
      path_tokens.append(str(context.get(JOBBER_CTX_PORT, JOBBER_PORT)))
    path_tokens.append(path)
    return urlparse(''.join(path_tokens))

  def host(self):
    return self._path.hostname

  def path(self):
    return self._path.path if len(self._path.path) > 0 else None

  def port(self):
    return self._path.port
