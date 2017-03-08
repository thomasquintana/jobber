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

from threading import Thread

import unittest
from mock import create_autospec, Mock

from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_SCHEDULER_RUNNING,
        ACTOR_SCHEDULER_STOPPED, ACTOR_SCHEDULER_STOPPING)

from jobber.core.scheduler.shortest_job_next_scheduler import SJNScheduler
from jobber.core.actor.processor import ActorProcessor
from jobber.core.scheduler.actor_heap import ShortestJobNextHeap
from jobber.core.actor.actor import Actor
from jobber.core.messages.poison_pill import PoisonPill

from jobber.core.exceptions.no_messages_exception import NoMessagesException

class SJNSchedulerTests(unittest.TestCase):
    def setUp(self):
        self.scheduler = SJNScheduler()

        self.mock_actor_1 = Mock(Actor())
        self.mock_actor_2 = Mock(Actor())
        self.mock_actor_3 = Mock(Actor())
        self.processor_1 = ActorProcessor(self.mock_actor_1)
        self.processor_2 = ActorProcessor(self.mock_actor_2)
        self.processor_3 = ActorProcessor(self.mock_actor_3)

        self.processor_1._receive_message(MockMessage())
        self.processor_2._receive_message(MockMessage())
        self.processor_3._receive_message(PoisonPill())

    def test_schedules_processor_correctly(self):
        self.scheduler.schedule(self.processor_1)
        self.assertTrue(len(self.scheduler._processors) == 1)
        self.scheduler.schedule(self.processor_2)
        self.assertTrue(len(self.scheduler._processors) == 2)
        self.scheduler.schedule(self.processor_3)
        self.assertTrue(len(self.scheduler._processors) == 3)

    def test_execute_message(self):
        self.scheduler.schedule(self.processor_1)
        self.scheduler.schedule(self.processor_2)

        (processor, message) = self.scheduler._processors.pop()
        self.scheduler._execute_message(processor, message)
        self.assertTrue(self.scheduler._processors.first() == self.processor_2)
        self.mock_actor_1.receive.assert_called_once()

    def test_execute_removes_completed_actor(self):
        self.processor_3.stop = Mock(self.processor_3.stop)
        self.scheduler.schedule(self.processor_3)

        (processor, message) = self.scheduler._processors.pop()
        self.scheduler._execute_message(processor, message)

        self.processor_3.stop.assert_called_once()
        with self.assertRaises(NoMessagesException):
            self.scheduler._processors.first()

    def test_run_does_nothing_if_stopped(self):
        self.processor_1.execute = Mock()
        self.scheduler.schedule(self.processor_1)

        self.scheduler._state = 'not ACTOR_SCHEDULER_STOPPED'
        thread = Thread(target=self.scheduler.start)
        thread.start()

        self.scheduler.shutdown()
        thread.join()

        self.processor_1.execute.assert_not_called()

    def test_scheduler_run_processes_all_messages(self):
        self.scheduler.schedule(self.processor_1)
        self.scheduler.schedule(self.processor_2)

        thread = Thread(target=self.scheduler.start)
        thread.start()

        self.scheduler.shutdown()
        thread.join()

        self.assertTrue(self.processor_1.pending_message_count == 0)
        self.assertTrue(self.processor_2.pending_message_count == 0)

class SJNSchedulingTests(unittest.TestCase):
    def test_10_by_10_test(self):
        AMOUNT_PROCESSORS = 10
        AMOUNT_MESSAGES = 10
        scheduler = SJNScheduler()

        mock_actor = create_autospec(Actor())
        processors = [ActorProcessor(mock_actor) for _ in range(AMOUNT_PROCESSORS)]
        for processor in processors:
            for _ in range(AMOUNT_MESSAGES):
                processor._receive_message(MockMessage())

        for processor in processors:
            scheduler.schedule(processor)

        thread = Thread(target=scheduler.start)
        thread.start()

        scheduler.shutdown()
        thread.join()

        self.assertTrue(mock_actor.receive.call_count == AMOUNT_PROCESSORS*AMOUNT_MESSAGES)

class MockMessage(object):
    pass
