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

from jobber.actors.exceptions import InterruptException
from jobber.actors.executable import Task
from jobber.actors.messages.poison_pill import PoisonPill

class ActorRef(Task):
  '''
  
  Positional Arguments:
  actor   --   A reference to the actor or a proxy actor.
  path    --   A valid url path to the referenced actor.
  scheduler -- The scheduler responsible for the exection of this actor.
  '''

  def __init__(self, actor, path, scheduler):
    super(ActorRef, self).__init__()
    self._logger = logging.getLogger(self.fqn)
    self._actor = actor
    self._mailbox = list()
    self._path = path
    self._scheduler = scheduler
    self._state = Task.Idle
    self._urn = uuid4()
    # NOTE: This is typically bad and should make your linter complain.
    # Monkey patch the actor.
    self._actor._actor_ref = self
    # Schedule ourselves for execution.
    self._scheduler.schedule(self)

  def __getattr__(self, name):
    if name == "path":
      return self._path.geturl()
    elif name == "state":
      return self._state
    elif name == "urn":
      return self._urn

  def run(self):
    while True:
      if len(self._mailbox) == 0:
        self._state = Task.Idle
        break
      else:
        self._state = Task.Running
        # Take a message from the head of the queue.
        message = self._mailbox.pop(0)
        # If we get a poison pill we must die.
        if isinstance(message, PoisonPill):
          self._scheduler.unschedule(self)
          self._state = Task.Completed
          # If the actor defined a stop method now is a good
          # time to call it.
          if hasattr(self._actor, "stop"):
            if callable(self._actor.stop):
              self._actor.stop()
          break
        # Process an incoming message.
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
          if len(self._mailbox) > 0:
            self._state = Task.Ready
          else:
            self._state = Task.Idle
          break

  def tell(self, message):
    self._mailbox.append(message)
    if self._state == Task.Idle:
      self._state = Task.Ready
