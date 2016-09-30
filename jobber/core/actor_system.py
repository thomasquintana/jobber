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
from urlparse import urlparse

from jobber.constants import JOBBER_CTX_HOSTNAME, JOBBER_CTX_PORT, \
                             JOBBER_PORT, JOBBER_SCHEME
from jobber.errors import ACTOR_REF_INVALID_PATH, ACTOR_REF_INVALID_SCHEME, \
                          ACTOR_SYSTEM_INVALID_PROC_COUNT

class ActorSystem(object):
  def __init__(self, router, scheduler):
    super(ActorSystem, self).__init__()
    self._router = router
    self._scheduler = scheduler

  def _generate_path(self, parent_ref):
    pass

  def _validate_path(self, context, path):
    if len(path.path) == 0:
      raise ValueError(ACTOR_REF_INVALID_PATH)
    if not path.scheme == JOBBER_SCHEME:
      raise ValueError(ACTOR_REF_INVALID_SCHEME)

  @staticmethod
  def bootstrap_process(name, pipes):
    pass

  @staticmethod
  def bootstrap_system(address=None, port=None, proc_count=None):
    if proc_count <= 0:
      raise ValueError(ACTOR_SYSTEM_INVALID_PROC_COUNT)
    neighbor_count = proc_count - 1
    if neighbor_count > 0:
      # Create the necessary bi-directional pipe groups to wire the
      # processes up in a start topology.
      proc_ends = [list() * proc_count]
      if proc_count == 2:
        (end0, end1) = Pipe(True)
        proc_ends[0].append(end0)
        proc_ends[1].append(end1)
      else:
        pipe_count = (proc_count * (proc_count - 1)) / 2
        # Group the outside edges first.
        for idx in xrange(proc_count - 1):
          (end0, end1) = Pipe(True)
          proc_ends[idx].append(end0)
          proc_ends[idx + 1].append(end1)
        (end0, end1) = Pipe(True)
        proc_ends[proc_count - 1].append(end0)
        proc_ends[0].append(end1)
        # If the number of processes is great than three then group
        # the adjacent edges.
        if proc_count > 3:
          pass


    # # Start the system processes and wire them up.
    # proc_count = proc_count if proc_count else cpu_count()
    # proc_count -= 1
    # processes = list()
    # for proc_idx in xrange(proc_count):
    #   proc_name = "process-%s" % proc_idx
    #   processes.append(Process(
    #     args=(proc_name, read_pipes[proc_idx], write_pipes[proc_idx]),
    #     kwargs={}, name=proc_name, target=ActorSystem.bootstrap_process
    #   ))

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

  def shutdown(self):
    pass
