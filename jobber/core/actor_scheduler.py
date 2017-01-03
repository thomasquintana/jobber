
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

from jobber.core.exceptions.interrupt_exception import InterruptException
from jobber.core.messages.poison_pill import PoisonPill
from jobber.constants import ACTOR_PROCESSOR_IDLE, ACTOR_PROCESSOR_READY
from jobber.utils import format_ms, object_fqn, time_delta_ms

class ActorScheduler(object):
  def __init__(self, max_msgs_slice, max_time_slice):
    super(ActorScheduler, self).__init__()
    self._logger = logging.getLogger(object_fqn(self))
    self._max_msgs_slice = max_msgs_slice
    self._max_time_slice = max_time_slice # In milliseconds.
    # Scheduler run-time state.
    self._curr_actor_proc = None
    self._idle_actor_procs = list()
    self._ready_actor_procs = list()
    self._waiting_actor_procs = list()
    self._running = False
    # Run-time statistics.
    self._start_run_time = 0.
    self._stop_run_time = 0.
    self._total_msgs_processed = 0

  def _run(self):
    n_running_actors = len(self._idle_actor_procs) + \
                       len(self._ready_actor_procs) + \
                       len(self._waiting_actor_procs)
    self._start_run_time = time.time()
    while self._running or n_running_actors > 0:
      # Check the idle actor processors list for actors with new messages.
      if len(self._idle_actor_procs) > 0:
        temp = list()
        for actor_proc in self._idle_actor_procs:
          if actor_proc.pending_msg_count == 0:
            temp.append(actor_proc)
          else:
            self._waiting_actor_procs.append(actor_proc)
        self._idle_actor_procs = temp
      # Update the current ready queue.
      self._ready_actor_procs = self._waiting_actor_procs
      self._waiting_actor_procs = list()
      # If we don't have work to do back off for random periods of time
      # that never exceed one second at a time.
      if len(self._ready_actor_procs) == 0:
        time.sleep(1 * random.uniform(0, 1))
        continue
      # Once we have some work to do allow actor processors in the current
      # ready queue to take over the process.
      while len(self._ready_actor_procs) > 0:
        self._curr_actor_proc = self._ready_actor_procs.pop(0)
        # If the current actor was penalized on a previous run it will be
        # skipped until the slice penalty is adjusted to 0. If there is no
        # penalty the actor is handed the CPU
        if self._curr_actor_proc.slice_penalty > 0:
          self._curr_actor_proc.slice_penalty -= 1
          self._waiting_actor_procs.append(self._curr_actor_proc)
        else:
          self._curr_actor_proc.execute()
          # Update our run-time statistics.
          self._total_msgs_processed += self._curr_actor_proc.slice_msg_count
          # Make sure we penalize CPU hogs.
          delta = self._max_time_slice - self._curr_actor_proc.slice_run_time
          if delta < 0 and abs(delta) > self._max_time_slice * .1:
            self._curr_actor_proc.slice_penalty = int(
              self._curr_actor_proc.slice_run_time / self._max_time_slice
            )
          # Move the actor processor to the next ready queue or the idle
          # queue if it doesn't have anymore messages to process.
          if self._curr_actor_proc.state == ACTOR_PROCESSOR_IDLE:
            self._idle_actor_procs.append(self._curr_actor_proc)
          elif self._curr_actor_proc.state == ACTOR_PROCESSOR_READY:
            self._waiting_actor_procs.append(self._curr_actor_proc)
      # Update the number of running actors.
      n_running_actors = len(self._idle_actor_procs) + \
                         len(self._ready_actor_procs) + \
                         len(self._waiting_actor_procs)
    self._stop_run_time = time.time()

  def interrupt(self):
    # Constrain the actor to the max time slice.
    if self._curr_actor_proc.slice_run_time >= self._max_time_slice:
      raise InterruptException()
    # Constrain the actor to the max number of messages per time slice.
    elif self._curr_actor_proc.slice_msg_count == self._max_msgs_slice:
      raise InterruptException()

  def schedule(self, actor_proc):
    self._idle_actor_procs.append(actor_proc)

  def shutdown(self):
    # Stop all the actor processors.
    actor_procs = self._waiting_actor_procs + self._idle_actor_procs + \
                  self._ready_actor_procs
    poison_pill = PoisonPill()
    for actor_proc in actor_procs:
      actor_proc.tell(poison_pill)
    self._running = False

  def start(self):
    self._running = True
    self._run()

  @property
  def total_msgs_processed(self):
    return self._total_msgs_processed

  @property
  def total_run_time(self):
    total_run_time = 0
    if not self._start_run_time is None:
      if self._stop_run_time is None:
        total_run_time = time_delta_ms(self._start_run_time, time.time())
      else:
        total_run_time = time_delta_ms(
          self._start_run_time, self._stop_run_time
        )
    return total_run_time

  @property
  def total_run_time_str(self):
    return format_ms(time_delta_ms(self._start_run_time, time.time()))
