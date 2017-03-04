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

import time
import unittest

from builtins import range
from threading import Thread
from unittest import TestCase

try:
    from unittest.mock import create_autospec, Mock
except ImportError:
    from mock import create_autospec, Mock

from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE,
        ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING)

from jobber.core.actor.actor import Actor
from jobber.core.actor.mailbox import Mailbox
from jobber.core.actor.actor_processor import ActorProcessor
from jobber.core.scheduler.actor_scheduler import ActorScheduler
from jobber.core.exceptions.interrupt_exception import InterruptException
from jobber.core.messages.poison_pill import PoisonPill

class ActorSchedulerTests(TestCase):
    def setUp(self):
        self._scheduler = ActorScheduler(10)
        self._thread = Thread(target=self._scheduler.start)
        self._thread.start()

    def test_actor_scheduler_one_processor(self):
        actor = Actor()
        actor.receive = Mock(return_value=None)
        actor.receive.side_effect = lambda message: len(message)

        mailbox = Mailbox()
        for _ in range(100):
            mailbox.append('jobber')

        processor = ActorProcessor(actor, mailbox, self._scheduler)
        processor.start()

        self._scheduler.shutdown()
        self._thread.join()
        self.assertTrue(actor.receive.call_count == 100)

    @unittest.skip('test does not work')
    def test_actor_scheduler_many_processors(self):
        AMOUNT_ACTORS = 100
        MAILBOX_LENGTH = 100

        actors = list()
        for _ in range(AMOUNT_ACTORS):
            actor = Actor()
            actor.receive = Mock(return_value=None)
            actor.receive.side_effect = lambda message: len(message)
            actors.append(actor)

        mailboxes = [Mailbox() for _ in range(AMOUNT_ACTORS)]
        for mailbox in mailboxes:
            for _ in range(MAILBOX_LENGTH):
                mailbox.append('jobber')
        processors = list()
        for index in range(AMOUNT_ACTORS):
            processor = ActorProcessor(actors[index], mailboxes[index], self._scheduler)
            processor.start()
            processors.append(processor)

        self._scheduler.shutdown_now()
        self._thread.join()
        for actor in actors:
            self.assertTrue(actor.receive.call_count == MAILBOX_LENGTH)


if __name__ == '__main__':
  unittest.main()
