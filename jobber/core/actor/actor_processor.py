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

from jobber.core.exceptions.interrupt_exception import InterruptException
from jobber.core.messages.poison_pill import PoisonPill
from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE,
        ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING)

from jobber.utils import object_fully_qualified_name

class ActorProcessor(object):
    """
    An actor processor is responsible for mapping individual actors to
    processes that can run the actor. The actor processor works in conjunction
    with the scheduler to provide fair resource distribution between all
    the actors managed by a particular scheduler.
    """

    def __init__(self, actor, mailbox, scheduler):
        super(ActorProcessor, self).__init__()
        self._logger = logging.getLogger(object_fully_qualified_name(self))
        self._actor = actor
        self._actor.processor = self

        self._mailbox = mailbox
        self._scheduler = scheduler
        self._state = None

    def execute(self):
        """
        This method will be scheduled for execution by the scheduler.
        """

        while True:
            if len(self._mailbox) == 0:
                self._state = ACTOR_PROCESSOR_IDLE
                break

            self._state = ACTOR_PROCESSOR_RUNNING
            message = self._mailbox.pop()

            if isinstance(message, PoisonPill):
                self.stop()
                break
            try:
                self._actor.receive(message)
            except Exception as exception:
                self._logger.exception(exception)

            # Try to yield the process to the scheduler so it can run other tasks.
            # If the scheduler raises an InterruptException we break out of our
            # loop otherwise we continue processing messages.
            try:
                self._scheduler.interrupt()
            except InterruptException:
                if len(self._mailbox) > 0:
                    self._state = ACTOR_PROCESSOR_READY
                else:
                    self._state = ACTOR_PROCESSOR_IDLE
                break

    @property
    def pending_message_count(self):
        return len(self._mailbox)

    def start(self):
        if hasattr(self._actor, "on_start"):
            if callable(self._actor.on_start):
                self._actor.on_start()

        self._state = ACTOR_PROCESSOR_IDLE
        self._scheduler.schedule(self)

    @property
    def state(self):
        return self._state

    def stop(self):
        self._state = ACTOR_PROCESSOR_COMPLETED
        if hasattr(self._actor, 'on_stop'):
            if callable(self._actor.on_stop):
                self._actor.on_stop()

    def stop_gracefully(self):
        self._mailbox.append(PoisonPill())

    def _receive_message(message):
        self._mailbox.append(message)
