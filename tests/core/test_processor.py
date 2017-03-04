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

from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE,
        ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING)

from jobber.core.actor.processor import ActorProcessor
from jobber.core.actor.actor import Actor
from jobber.core.actor.mailbox import Mailbox
from jobber.core.scheduler.scheduler import Scheduler

from mock import create_autospec, Mock

class ProcessorTests(unittest.TestCase):
    def setUp(self):
        self.mock_actor = create_autospec(Actor)
        self.mock_actor.on_start = Mock(return_value=None)
        self.mock_actor.on_stop = Mock(return_value=None)

        self.mock_mailbox = create_autospec(Mailbox)
        self.mock_scheduler = create_autospec(Scheduler)
        self.processor = ActorProcessor(self.mock_actor, self.mock_mailbox, self.mock_scheduler)

    def test_pending_message_count(self):
        self.assertTrue(self.processor.pending_message_count == 0)
        self.mock_mailbox.__len__.assert_called_once()

    def test_state(self):
        self.processor._state = 'some state'
        self.assertTrue(self.processor._state == self.processor.state)

    def test_start_happy_path(self):
        self.processor.start()

        self.assertTrue(self.processor.state == ACTOR_PROCESSOR_IDLE)
        self.mock_actor.on_start.assert_called_once()
        self.mock_scheduler.schedule.assert_called_once()

    def test_stop(self):
        self.processor.stop()

        self.mock_actor.on_stop.assert_called_once()
        self.assertTrue(self.processor.state == ACTOR_PROCESSOR_COMPLETED)

    def test_stop_gracefully(self):
        self.processor.stop_gracefully()
        self.mock_mailbox.append.assert_called_once()

    def test_receive_message(self):
        self.processor._receive_message('some message')
        self.mock_mailbox.append.assert_called_once()
