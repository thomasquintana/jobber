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
import time

from jobber.core.exceptions import InterruptException
from jobber.core.messages.poison_pill import PoisonPill
from jobber.constants import ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE, \
                             ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING
from jobber.utils import object_fqn, time_delta_ms

class ActorProcessor(object):
  '''
  An actor processor is responsible for mapping individual actors to
  processes that can run the actor. The actor processor works in conjunction
  with the scheduler to provide fair resource distribution between all
  the actors managed by a particular scheduler.
  '''

  def __init__(self, actor, mailbox, scheduler, urn):
    super(ActorProcessor, self).__init__()
    self._logger = logging.getLogger(object_fqn(self))
    self._actor = actor
    self._mailbox = mailbox
    self._scheduler = scheduler
    self._state = None
    self._urn = urn
    # Run-time statistics.
    self._slice_msg_count = 0
    self._slice_penalty = 0
    self._slice_run_time = 0
    self._total_msg_count = 0
    self._total_run_time = 0

  def __getattr__(self, name):
    if name == "adjusted_priority":
      return self._adj_priority
    elif name == "pending_msg_count":
      return len(self._mailbox)
    elif name == "slice_msg_count":
      return self._slice_msg_count
    elif name == "slice_penalty":
      return self._slice_penalty
    elif name == "slice_run_time":
      return self._slice_run_time
    elif name == "state":
      return self._state
    elif name == "total_msg_count":
      return self._total_msg_count
    elif name == "total_run_time":
      return self._total_run_time
    elif name == "urn":
      return self._urn

  def __setattr__(self, name, value):
    if name == "slice_penalty":
      self._slice_penalty = value

  def execute(self):
    '''
    This method will be scheduled for execution by the scheduler..
    '''

    self._slice_msg_count = 0
    self._slice_run_time = 0
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
        start_time = time.time()
        try:
          self._actor.receive(message)
        except Exception as exception:
          self._logger.exception(exception)
        end_time = time.time()
        # Update the slice statistics before we call the scheduler's
        # interrupt() method.
        self._slice_msg_count += 1
        self._slice_run_time += time_delta_ms(start_time, end_time)
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
    self._total_msg_count += self._slice_msg_count
    self._total_run_time += self._slice_run_time

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
    # If the actor defined an on_stop method now is a good
    # time to call it.
    if hasattr(self._actor, "on_stop"):
      if callable(self._actor.on_stop):
        self._actor.on_stop()
