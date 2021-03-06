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

from jobber.core.actor.processor import ActorProcessor, NO_MESSAGES_RUNTIME
from jobber.core.actor.actor import Actor
from jobber.core.actor.mailbox import Mailbox
from jobber.core.scheduler.runtime_dict import RuntimeDict

from mock import create_autospec, Mock

class ProcessorTests(unittest.TestCase):
    def setUp(self):
        self.mock_actor = create_autospec(Actor)
        self.mock_actor.on_start = Mock(return_value=None)
        self.mock_actor.on_stop = Mock(return_value=None)

        self.mock_mailbox = create_autospec(Mailbox)
        self.processor = ActorProcessor(self.mock_actor)
        self.processor._mailbox = self.mock_mailbox

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

    def test_expected_next_runtime_no_messages(self):
        self.processor = ActorProcessor(self.mock_actor)
        self.processor.set_message_statistics(RuntimeDict())
        self.assertTrue(self.processor.expected_next_runtime() == NO_MESSAGES_RUNTIME)

    def test_expected_next_runtime(self):
        self.processor = ActorProcessor(self.mock_actor)
        self.processor.set_message_statistics(RuntimeDict())
        self.processor._mailbox.append(MockMessage())
        self.assertTrue(self.processor.expected_next_runtime() == 0.0)

        self.processor._message_statistics.update(MockMessage, 3.0)
        self.assertTrue(self.processor.expected_next_runtime() == 3.0)
        self.processor._message_statistics.update(MockMessage, 5.0)
        self.assertTrue(self.processor.expected_next_runtime() == 4.0)
        self.processor._message_statistics.update(MockOtherMessage, 2.0)
        self.assertTrue(self.processor.expected_next_runtime() == 4.0)

class ProcessorCMPTests(unittest.TestCase):
    def setUp(self):
        self.mock_actor = create_autospec(Actor)
        self.processor = ActorProcessor(self.mock_actor)
        self.other_processor = ActorProcessor(self.mock_actor)

        runtime_dict = RuntimeDict()
        runtime_dict.update(MockMessage, 2.0)
        runtime_dict.update(MockOtherMessage, 1.0)

        self.processor.set_message_statistics(runtime_dict)
        self.other_processor.set_message_statistics(runtime_dict)

    def test_equality(self):
        self.assertTrue(self.processor == self.processor)
        self.assertTrue(self.processor != self.other_processor)

    def test_message_order(self):
        self.processor._receive_message(MockMessage())
        self.assertTrue(self.processor < self.other_processor)

class MockMessage(object):
    pass

class MockOtherMessage(object):
    pass
