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
import time

from threading import Event

from sortedcontainers import SortedListWithKey

from jobber.core.exceptions.interrupt_exception import InterruptException
from jobber.core.exceptions.scheduler_stopped_exception import SchedulerStoppedException
from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_SCHEDULER_RUNNING,
        ACTOR_SCHEDULER_STOPPED, ACTOR_SCHEDULER_STOPPING)

from jobber.utils import object_fully_qualified_name

class Scheduler(object):
    """
    Minimal Scheduler Interface
    """

    def __init__(self):
        super(Scheduler, self).__init__()
        self._logger = logging.getLogger(object_fully_qualified_name(self))
        self._state = ACTOR_SCHEDULER_STOPPED
        self._processors = list()

    def _run(self):
        """
        Implements the scheduling function
        """
        pass

    def schedule(self, actor_processor):
        """
        Schedules an Actor Processor for Message Processing
        """
        pass

    def shutdown(self):
        if self._state == ACTOR_SCHEDULER_RUNNING:
            for processor in self._processors:
                processor.stop_gracefully()

            self._state = ACTOR_SCHEDULER_STOPPING

    def shutdown_now(self):
        self._state = ACTOR_SCHEDULER_STOPPED
        for processor in self._processors:
            processor.stop()

    def start(self):
        if self._state == ACTOR_SCHEDULER_STOPPED:
            self._state = ACTOR_SCHEDULER_RUNNING
            self._run()
