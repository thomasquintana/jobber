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

from multiprocessing import cpu_count
from urlparse import urlparse

from jobber.constants import JOBBER_CTX_HOSTNAME, JOBBER_CTX_PORT, \
                             JOBBER_PORT, JOBBER_SCHEME
from jobber.errors import ACTOR_REF_INVALID_PATH, ACTOR_REF_INVALID_SCHEME

class ActorSystem(object):
  def __init__(self, address, port=5555, proc_count=None):
    super(ActorSystem, self).__init__()
    self._address = address
    self._port = port
    self._proc_count = proc_count or cpu_count()

  def _generate_path(self, parent_ref):
    pass

  def _validate_path(self, context, path):
    if len(path.path) == 0:
      raise ValueError(ACTOR_REF_INVALID_PATH)
    if not path.scheme == JOBBER_SCHEME:
      raise ValueError(ACTOR_REF_INVALID_SCHEME)

  def bootstrap(self, address, port, proc_count=None):
    pass

  def create(self, fqn, *args, **kwargs):
    # Load object.
    # Validate that it's an actor and implements receive and receive is callable.
    # Create actor reference

    # NOTE: This is typically bad and should make your linter complain.
    # Monkey patch the actor.
    #self._actor.parent_ref = parent_ref
    #self._actor.actor_ref = actor_ref
    #self._actor.actor_system = self

    
    # Create actor processor
    # Start the actor processor
    # Return the actor reference.
    pass

  def locate(self, path):
    pass
