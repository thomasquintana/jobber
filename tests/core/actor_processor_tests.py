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

from builtins import range
from unittest import TestCase
try:
  from unittest.mock import create_autospec, Mock
except ImportError:
  from mock import create_autospec, Mock

from jobber.constants import ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE, \
                             ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING
from jobber.core.actor import Actor
from jobber.core.actor_processor import ActorProcessor
from jobber.core.actor_scheduler import ActorScheduler
from jobber.core.exceptions.interrupt_exception import InterruptException
from jobber.core.messages.poison_pill import PoisonPill

class ActorProcessorTests(TestCase):
  def setUp(self):
    self._actor = Actor()
    self._mailbox = list()
    self._scheduler = create_autospec(ActorScheduler)
    self._processor = ActorProcessor(
      self._actor, self._mailbox, self._scheduler
    )

  def test_actor_lifecycle_method_invocation(self):
    self._actor.on_start = Mock(return_value=None)
    self._actor.on_stop = Mock(return_value=None)
    self._processor.start()
    self._actor.on_start.assert_called_once()
    self._processor.stop()
    self._actor.on_stop.assert_called_once()

  def test_actor_entry_point_method_invocation(self):
    self._actor.receive = Mock(return_value=None)
    self._processor.start()
    self._mailbox.append("jobber")
    self._processor.execute()
    self._actor.receive.assert_called_once()
    self.assertTrue(self._processor.pending_msg_count == 0)
    self._processor.stop()

  def test_actor_processor_empty_mailbox(self):
    self._processor.start()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._processor.execute()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._processor.stop()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_COMPLETED)

  def test_actor_processor_one_message(self):
    self._processor.start()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._mailbox.append("jobber")
    self._processor.execute()
    self._scheduler.interrupt.assert_called_once()
    self.assertTrue(self._processor.pending_msg_count == 0)
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._processor.stop()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_COMPLETED)

  def test_actor_processor_interrupted_no_pending_message(self):
    self._processor.start()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._mailbox.append("jobber")
    self._scheduler.interrupt.side_effect = InterruptException()
    self._processor.execute()
    self._scheduler.interrupt.assert_called_once()
    self.assertTrue(self._processor.pending_msg_count == 0)
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._processor.stop()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_COMPLETED)

  def test_actor_processor_interrupted_pending_message(self):
    self._processor.start()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._mailbox.append("jobber")
    self._mailbox.append("jobber")
    self._scheduler.interrupt.side_effect = InterruptException()
    self._processor.execute()
    self._scheduler.interrupt.assert_called_once()
    self.assertTrue(self._processor.pending_msg_count == 1)
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_READY)
    self._processor.stop()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_COMPLETED)

  def test_actor_processor_poison_pill(self):
    self._processor.start()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_IDLE)
    self._mailbox.append(PoisonPill())
    self._processor.execute()
    self.assertTrue(self._processor.state == ACTOR_PROCESSOR_COMPLETED)

if __name__ == '__main__':
  unittest.main()
