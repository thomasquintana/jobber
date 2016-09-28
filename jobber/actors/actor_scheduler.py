
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
import random
import time

from jobber.actors.exceptions import InterruptException
from jobber.constants import ACTOR_PROCESSOR_IDLE, ACTOR_PROCESSOR_READY
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
    self._idle_actor_procs = list()
    self._curr_ready_actor_procs = list()
    self._next_ready_actor_procs = list()
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
      # Check the idle actor processors list for actors with new messages.
      if len(self._idle_actor_procs) > 0:
        temp = list()
        for actor_proc in self._idle_actor_procs:
          if actor_proc.pending_msg_count == 0:
            temp.append(actor_proc)
          else:
            self._next_ready_actor_procs.append(actor_proc)
        self._idle_actor_procs = temp
      # Update the current ready queue.
      self._curr_ready_actor_procs = self._next_ready_actor_procs
      self._next_ready_actor_procs = list()
      # If we don't have work to do back off for random periods of time
      # that never exceed one second at a time.
      if len(self._curr_ready_actor_procs) == 0:
        time.sleep(1 * random.uniform(0, 1))
        continue
      # Once we have some work to do allow actor processors in the current
      # ready queue to take over the process.
      while len(self._curr_ready_actor_procs) > 0:
        self._current_actor_proc = self._curr_ready_actor_procs.pop(0)
        # Hand over the process to the current actor processor.
        self._current_actor_proc.execute()
        # Move the actor processor to the next ready queue or the idle
        # queue if it doesn't have anymore messages to process.
        if self._current_actor_proc.state == ACTOR_PROCESSOR_IDLE:
          self._idle_actor_procs.append(self._current_actor_proc)
        elif self._current_actor_proc.state == ACTOR_PROCESSOR_READY:
          self._next_ready_actor_procs.append(self._current_actor_proc)

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
    self._idle_actor_procs.append(actor_proc)

  def shutdown(self):
    self._running = False

  def start(self):
    self._start_run_time = time.time()
    self._run()
