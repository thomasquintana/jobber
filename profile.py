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

"""
Simulates the overhead of a system with 10000 actors that do nothing
Each processing 1000 messages and then shutting down.

Run with command:
python -m cProfile -s time profile.py
"""

AMOUNT_PROCESSORS = 10000
AMOUNT_MESSAGES = 1000

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

class MockMessage(object):
    pass

def stresstest():
    scheduler = SJNScheduler()

    mock_actor = create_autospec(Actor())
    processors = [ActorProcessor(mock_actor) for _ in range(AMOUNT_PROCESSORS)]
    for processor in processors:
        for _ in range(AMOUNT_MESSAGES):
            processor._receive_message(MockMessage())

    for processor in processors:
        scheduler.schedule(processor)

    scheduler._state = ACTOR_SCHEDULER_RUNNING
    scheduler.shutdown()
    scheduler._state == ACTOR_SCHEDULER_STOPPED
    scheduler.start()

if __name__=='__main__':
    stresstest()
