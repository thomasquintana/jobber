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

from multiprocessing import cpu_count, Pipe, Process

from jobber.constants import JOBBER_PORT, JOBBER_SCHEME
from jobber.core.actor_scheduler import ActorScheduler
from jobber.core.message_router import MessageRouter
from jobber.errors import ACTOR_REF_INVALID_PATH, ACTOR_REF_INVALID_SCHEME, \
                          ACTOR_SYSTEM_INVALID_PROC_COUNT

class ActorSystem(object):
  def __init__(self, name, conns, max_msgs_slice, max_time_slice,
               address=None, port=None):
    super(ActorSystem, self).__init__()
    self._proxy = None
    self._router = None
    self._scheduler = ActorScheduler(max_msgs_slice, max_time_slice)

  def _generate_path(self, parent_ref):
    pass

  def _validate_path(self, context, path):
    if len(path.path) == 0:
      raise ValueError(ACTOR_REF_INVALID_PATH)
    if not path.scheme == JOBBER_SCHEME:
      raise ValueError(ACTOR_REF_INVALID_SCHEME)
    

  @staticmethod
  def bootstrap_system(address=None, port=None, max_msgs_slice=10, \
                       max_time_slice=50, proc_count=None):
    if proc_count is None or proc_count <= 0:
      raise ValueError(ACTOR_SYSTEM_INVALID_PROC_COUNT)
    if proc_count - 1 > 0:
      # Create the necessary bi-directional pipe groups to wire the
      # processes up in a star topology.
      proc_ends = [list() * proc_count]
      if proc_count == 2:
        (end0, end1) = Pipe(True)
        proc_ends[0].append(end0)
        proc_ends[1].append(end1)
      else:
        for proc_idx in xrange(proc_count - 1):
          missing_conn_count = proc_count - (proc_idx + 1)
          for neighbor_idx in xrange(1, missing_conn_count):
            (end0, end1) = Pipe(True)
            proc_ends[proc_idx].append(end0)
            proc_ends[proc_idx + neighbor_idx].append(end1)
        (end0, end1) = Pipe(True)
        proc_ends[proc_count - 1].append(end0)
        proc_ends[0].append(end1)
      # Bootstrap all the child processes.
      proc_count = proc_count if proc_count else cpu_count()
      for proc_idx in xrange(1, proc_count - 1):
        proc_name = "jobber-%s" % proc_idx
        proc = ActorSystem(
          proc_name, proc_ends[proc_idx], max_msgs_slice, max_time_slice,
          address=address, port=port
        )
        Process(name=proc_name, target=proc.start)
    # Bootstrap this process and have it join the other processes.
    actor_system = ActorSystem(
      "jobber-0", proc_ends[0], max_msgs_slice, max_time_slice,
      address=address, port=port
    )
    actor_system.start()

  def create(self, fqn, *args, **kwargs):
    # Load object.
    # Validate that it's an actor and implements receive and receive is callable.
    # Create actor reference

    # NOTE: This is typically bad and should make your linter complain.
    # Monkey patch the actor.
    #self._actor.parent_ref = parent_ref
    #self._actor.actor_ref = actor_ref
    #self._actor.actor_system = self
    
    # Create actor processor
    # Start the actor processor
    # Return the actor reference.
    pass

  def locate(self, path):
    pass

  def start(self):
    # TODO: Create the necessary items.
    # Start the scheduler.
    self._scheduler.start()

  def shutdown(self):
    pass
