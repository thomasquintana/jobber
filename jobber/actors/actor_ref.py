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

import logging

from uuid import uuid4

from exceptions import InterruptException
from executable import Task

class ActorRef(Task):
  '''
  
  Positional Arguments:
  actor   -- A reference to the actor or a proxy actor.
  context -- A dictionary container holding the context state.
  path    -- A valid url path to the referenced actor.
  '''

  def __init__(self, actor, path, scheduler):
    super(ActorRef, self).__init__()
    self._logger = logging.getLogger(self.fqn)
    self._actor = actor
    self._mailbox = list()
    self._path = path
    self._scheduler = scheduler
    self._urn = uuid4()

  def __getattr__(self, name):
    if name == "path":
      return self._path.geturl()
    elif name == "urn":
      return self._urn

  def run(self):
    while len(self._mailbox) > 0:
      message = self._mailbox.pop(0)
      try:
        self._actor.receive(message)
      except Exception as exception:
        self._logger.exception(exception)
      # Try to return control of the processor to the scheduler if
      # the scheduler fires an InterruptException we hand over control
      # and if it doesn't we keep processing messages.
      try:
        self._scheduler.interrupt()
      except InterruptException:
        break

  def tell(self, message):
    self._mailbox.append(message)
