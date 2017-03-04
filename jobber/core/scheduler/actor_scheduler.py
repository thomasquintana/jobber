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
from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_SCHEDULER_RUNNING,
        ACTOR_SCHEDULER_STOPPED, ACTOR_SCHEDULER_STOPPING)

from jobber.utils import object_fully_qualified_name

class ActorScheduler(object):
    """
    A naive scheduler implementation for actors.
    """

    def __init__(self, slice_msgs):
        super(ActorScheduler, self).__init__()
        self._logger = logging.getLogger(object_fully_qualified_name(self))
        self._barrier = Event()
        self._processed_msgs = 0
        # Processes are stored as two-tuples (run-time, proc)
        # and we sort on run-time.
        self._procs = SortedListWithKey(key=lambda pd: pd[0])
        self._slice_msgs = slice_msgs
        self._state = ACTOR_SCHEDULER_STOPPED

    def _run(self):
        while True:
            print self._state, ",", len(self._procs)
            if self._state == ACTOR_SCHEDULER_STOPPING:
                if len(self._procs) == 0:
                    self._state = ACTOR_SCHEDULER_STOPPED
                    break

            elif self._state == ACTOR_SCHEDULER_STOPPED:
                break

            if len(self._procs) > 0:
                procs = self._procs
                self._procs = SortedListWithKey(key=lambda pd: pd[0])
                while len(procs) > 0:
                    runtime, proc = procs.pop(0)
                    start_time = time.time()
                    proc.execute()
                    end_time = time.time()
                    if not proc.state == ACTOR_PROCESSOR_COMPLETED:
                        self._procs.add((runtime + (end_time - start_time), proc))

            else:
                self._barrier.wait()
                self._barrier.clear()

    def interrupt(self):
        self._processed_msgs += 1
        if self._processed_msgs == self._slice_msgs:
            self._processed_msgs = 0
            raise InterruptException()

    def schedule(self, actor_proc):
        if self._state == ACTOR_SCHEDULER_RUNNING:
            self._procs.add((0., actor_proc))
            self._barrier.set()

    def shutdown(self):
        if self._state == ACTOR_SCHEDULER_RUNNING:
            for _, proc in self._procs:
                proc.stop_gracefully()

            self._state = ACTOR_SCHEDULER_STOPPING
            if len(self._procs) == 0:
                self._barrier.set()

    def shutdown_now(self):
        if self._state == ACTOR_SCHEDULER_RUNNING:
            self._state = ACTOR_SCHEDULER_STOPPED
            if len(self._procs) == 0:
                self._barrier.set()

    def start(self):
        if self._state == ACTOR_SCHEDULER_STOPPED:
            self._state = ACTOR_SCHEDULER_RUNNING
            self._run()
