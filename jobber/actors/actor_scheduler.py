
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

from sortedcontainers import SortedDict

from jobber.actors.exceptions import InterruptException
from jobber.constants import ACTOR_PROCESSOR_COMPLETED, ACTOR_PROCESSOR_IDLE, \
                             ACTOR_PROCESSOR_READY, ACTOR_PROCESSOR_RUNNING
from jobber.utils import format_time_period, object_fqn

class ActorScheduler(object):
  def __init__(self, **kwargs):
    super(ActorScheduler, self).__init__()
    self._logger = logging.getLogger(object_fqn(self))
    # Scheduler state.
    self._max_msgs_per_slice = kwargs.get("max_msgs_per_slice", 10)
    self._max_time_per_slice = kwargs.get("max_time_per_slice", 50) # In ms.
    self._running = True
    # Current actor with control of the process.
    self._current_actor_proc = None
    # Actor processors.
    self._deleted_actor_procs = SortedDict(key=lambda ap: ap.urn)
    self._idle_actor_procs = list()
    self._curr_ready_actor_procs = SortedDict(key=lambda ap: ap.total_run_time)
    self._next_ready_actor_procs = SortedDict(key=lambda ap: ap.total_run_time)
    # Run-time statistics.
    self._start_run_time = 0.
    self._total_msgs_processed = 0

  def __getattr__(self, name):
    if name == "total_msgs_processed":
      return self._total_msgs_processed
    elif name == "total_run_time":
      return (time.time() - self._start_run_time) / 1e-6
    elif name == "total_run_time_str":
      return format_time_period((time.time() - self._start_run_time) / 1e-6)

  def _run(self):
    while self._running:
      pass

  def interrupt(self):
    # interrupt() is called after every message handled so we
    # keep track of the number of messages handled here.
    self._total_msgs_processed += 1
    # Make sure the actor hasn't used up more time than it was allowed.
    if self._current_actor_proc.last_run_time >= self._max_time_per_slice:
      raise InterruptException()
    # Make sure the actor hasn't gone over the message processing threshold.
    elif self._current_actor_proc.last_msg_count == self._max_msgs_per_slice:
      raise InterruptException()

  def schedule(self, actor_proc):
    if actor_proc.state == ACTOR_PROCESSOR_IDLE:
      pass # Insert into idle queue.
    elif actor_proc.state == ACTOR_PROCESSOR_READY:
      pass # Insert into ready queue.

  def shutdown(self):
    self._running = False

  def start(self):
    self._start_run_time = time.time()
    self._run()

  def unschedule(self, actor_proc):
    pass # Insert into the deleted queue.
