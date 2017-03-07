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

from jobber.core.actor.mailbox import Mailbox

NO_MESSAGES_RUNTIME = 10e9

class ActorProcessor(object):
    """
    An actor processor is responsible for mapping individual actors to
    processes that can run the actor. The actor processor works in conjunction
    with the scheduler to provide fair resource distribution between all
    the actors managed by a particular scheduler.
    """

    def __init__(self, actor):
        super(ActorProcessor, self).__init__()
        self._logger = logging.getLogger(object_fully_qualified_name(self))
        self._actor = actor
        self._actor.processor = self

        self._mailbox = Mailbox()
        self._state = None

        self._message_statistics = None

    @property
    def pending_message_count(self):
        return len(self._mailbox)

    @property
    def state(self):
        return self._state

    def execute(self, message):
        self._actor.receive(message)

    def start(self):
        try:
            self._actor.on_start()
        except AttributeError:
            # actor has no attribute on_start
            pass
        except TypeError:
            # on_start is not callable
            pass

        self._state = ACTOR_PROCESSOR_IDLE

    def stop(self):
        self._state = ACTOR_PROCESSOR_COMPLETED
        try:
            self._actor.on_stop()
        except AttributeError:
            # actor has no attribute on_stop
            pass
        except TypeError:
            # on_stop is not callable
            pass

    def stop_gracefully(self):
        self._mailbox.append(PoisonPill())

    def _receive_message(self, message):
        self._mailbox.append(message)

    def set_message_statistics(self, message_statistics):
        self._message_statistics = message_statistics

    def expected_next_runtime(self):
        if self.pending_message_count == 0:
            return NO_MESSAGES_RUNTIME

        next_message = self._mailbox.first()
        return self._message_statistics.get(type(next_message))

    def pop_message(self):
        return self._mailbox.pop()

    def completed(self):
        return self._state == ACTOR_PROCESSOR_COMPLETED

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)

    def __lt__(self, other):
        return self.expected_next_runtime() < other.expected_next_runtime()

    def __le__(self, other):
        return self.expected_next_runtime() <= other.expected_next_runtime()

    def __gt__(self, other):
        return self.expected_next_runtime() > other.expected_next_runtime()

    def __ge__(self, other):
        return self.expected_next_runtime() >= other.expected_next_runtime()

    def __len__(self):
        return len(self._mailbox)
