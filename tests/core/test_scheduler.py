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
from mock import create_autospec, Mock

from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_SCHEDULER_RUNNING,
        ACTOR_SCHEDULER_STOPPED, ACTOR_SCHEDULER_STOPPING)

from jobber.core.scheduler.scheduler import Scheduler
from jobber.core.actor.actor_processor import ActorProcessor

class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()

    def test_run(self):
        self.scheduler._run()

    def test_schedule(self):
        self.scheduler.schedule('some actor processor')

    def test_start_calls_run(self):
        self.scheduler._run = Mock(return_value=None)
        self.scheduler.start()
        self.scheduler._run.assert_called_once()

    def test_start_sets_running(self):
        self.scheduler.start()
        self.assertTrue(self.scheduler._state == ACTOR_SCHEDULER_RUNNING)

    def test_start_wrong_state_does_nothing(self):
        self.scheduler._state = ACTOR_SCHEDULER_RUNNING
        self.scheduler._run = Mock(return_value=None)
        self.scheduler.start()
        self.scheduler._run.assert_not_called()

    def test_shutdown_now(self):
        processors = []
        for _ in range(10):
            processors.append(create_autospec(ActorProcessor))
        self.scheduler._processors = processors

        self.scheduler.shutdown_now()

        self.assertTrue(self.scheduler._state == ACTOR_SCHEDULER_STOPPED)
        for processor in processors:
            processor.stop.assert_called_once()

    def test_shutdown(self):
        processors = []
        for _ in range(10):
            processors.append(create_autospec(ActorProcessor))
        self.scheduler._processors = processors

        self.scheduler._state = ACTOR_SCHEDULER_RUNNING
        self.scheduler.shutdown()

        self.assertTrue(self.scheduler._state == ACTOR_SCHEDULER_STOPPING)
        for processor in processors:
            processor.stop_gracefully.assert_called_once()
