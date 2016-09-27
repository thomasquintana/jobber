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

from jobber.actors.exceptions import InterruptException
from jobber.actors.messages.poison_pill import PoisonPill
from jobber.constants import ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE, \
                             ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING
from jobber.utils import object_fqn

class ActorProcessor(object):
  '''
  A task is a lightweight thread of execution.
  '''

  def __init__(self, actor, mailbox, scheduler, uuid, priority=1):
    super(ActorProcessor, self).__init__()
    self._logger = logging.getLogger(object_fqn(self))
    self._actor = actor
    self._mailbox = mailbox
    self._priority = priority
    self._scheduler = scheduler
    self._state = None
    self._urn = uuid

  def __getattr__(self, name):
    if name == "priority":
      return self._priority
    elif name == "state":
      return self._state
    elif name == "urn":
      return self._urn

  def execute(self):
    '''
    This method will be scheduled for execution by the scheduler..
    '''

    while True:
      if len(self._mailbox) == 0:
        self._state = ACTOR_PROCESSOR_IDLE
        break
      else:
        self._state = ACTOR_PROCESSOR_RUNNING
        # Take a message from the head of the queue.
        message = self._mailbox.pop(0)
        # If we get a poison pill we must die.
        if isinstance(message, PoisonPill):
          self.stop()
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
            self._state = ACTOR_PROCESSOR_READY
          else:
            self._state = ACTOR_PROCESSOR_IDLE
          break

  def start(self):
    # If the actor defined an on_start method now is a good
    # time to call it.
    if hasattr(self._actor, "on_start"):
      if callable(self._actor.on_start):
        self._actor.on_start()
    self._state = ACTOR_PROCESSOR_IDLE
    self._scheduler.schedule(self)

  def stop(self):
    self._state = ACTOR_PROCESSOR_COMPLETED
    self._scheduler.unschedule(self)
    # If the actor defined an on_stop method now is a good
    # time to call it.
    if hasattr(self._actor, "on_stop"):
      if callable(self._actor.on_stop):
        self._actor.on_stop()
