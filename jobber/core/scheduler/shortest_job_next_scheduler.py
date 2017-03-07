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

from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_SCHEDULER_RUNNING,
        ACTOR_SCHEDULER_STOPPED, ACTOR_SCHEDULER_STOPPING)

from jobber.core.scheduler.scheduler import Scheduler
from jobber.core.scheduler.actor_heap import ShortestJobNextHeap

from jobber.core.exceptions.no_messages_exception import NoMessagesException
from jobber.core.messages.poison_pill import PoisonPill

class SJNScheduler(Scheduler):
    def __init__(self):
        super(SJNScheduler, self).__init__()
        self._processors = ShortestJobNextHeap()

    def schedule(self, actor_processor):
        self._processors.insert(actor_processor)
        # TODO: restart the scheduler

    def _execute_message(self, processor, message):
        if isinstance(message, PoisonPill):
            self._processors.remove(processor)
            processor.stop()
        else:
            processor.execute(message)

    def _run(self):
        while len(self._processors):
            try:
                (processor, message) = self._processors.pop()
                self._execute_message(processor, message)
            except NoMessagesException:
                pass
        self._state = ACTOR_SCHEDULER_STOPPED
