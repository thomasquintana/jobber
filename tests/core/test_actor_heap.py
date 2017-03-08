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

import unittest
from mock import create_autospec, Mock

from jobber.core.scheduler.actor_heap import ShortestJobNextHeap
from jobber.core.actor.processor import ActorProcessor
from jobber.core.actor.actor import Actor
from jobber.core.actor.mailbox import Mailbox

from jobber.core.exceptions.no_messages_exception import NoMessagesException

class ShortestJobNextHeapTests(unittest.TestCase):
    def setUp(self):
        self.heap = ShortestJobNextHeap()
        self.actorprocessor = ActorProcessor(create_autospec(Actor))
        self.other_actorprocessor = ActorProcessor(create_autospec(Actor))

        self.heap.insert(self.actorprocessor)
        self.heap.insert(self.other_actorprocessor)

        self.mockmessage = MockMessage()
        self.mock_other_message = MockMessage()
        self.actorprocessor._receive_message(self.mockmessage)
        self.other_actorprocessor._receive_message(self.mock_other_message)

    def test_heap_insert(self):
        self.assertTrue(self.heap.first() == self.actorprocessor)

    def test_heap_empty_pop_raises(self):
        self.actorprocessor._mailbox = Mailbox()
        with self.assertRaises(NoMessagesException):
            self.heap.pop()

    def test_heap_pop_preserves_size(self):
        heap_size = len(self.heap)
        self.heap.pop()
        self.assertTrue(len(self.heap) == heap_size)

    def test_heap_pop_returns_top_actor(self):
        first = self.heap.first()
        (target_actor, _) = self.heap.pop()
        self.assertTrue(first == target_actor)

    def test_heap_pop_removes_message(self):
        self.heap.pop()
        self.assertTrue(len(self.actorprocessor) == 0)

    def test_heap_pop_returns_processor_message_tuple(self):
        (processor, message) = self.heap.pop()
        self.assertTrue(processor == self.actorprocessor)
        self.assertTrue(message == self.mockmessage)

    def test_heap_pop_preserves_heap_condition(self):
        self.heap.pop()
        self.assertTrue(self.heap.first() == self.other_actorprocessor)

class MockMessage(object):
    pass
