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

from jobber.constants import JOBBER_PORT, LOCAL_HOST
from jobber.core.actor_scheduler import ActorScheduler
from jobber.core.message_router import MessageRouter
from jobber.errors import ACTOR_REF_INVALID_PATH, ACTOR_REF_INVALID_SCHEME, \
                          ACTOR_SYSTEM_INVALID_PROC_COUNT

class ActorSystem(object):
  def __init__(self, name, connections, max_msgs_slice, max_time_slice,
               ip, port):
    super(ActorSystem, self).__init__()
    self._connections = connections
    self._name = name
    self._router = MessageRouter(name, ip, port, connections)
    self._router.on_start()
    self._scheduler = None
  
  @staticmethod
  def bootstrap_system(ip=LOCAL_HOST, port=JOBBER_PORT, max_msgs_slice=10, \
                       max_time_slice=50, proc_count=None):
    if proc_count is None:
      proc_count = cpu_count()
    else:
      if proc_count <= 0:
        raise ValueError(ACTOR_SYSTEM_INVALID_PROC_COUNT)
    proc_conns = None
    if proc_count > 1:
      # Create the necessary bi-directional pipe groups to wire the
      # processes up in a star topology.
      proc_conns = [list() for _ in xrange(proc_count)]
      for proc_idx in xrange(proc_count - 1):
        missing_conn_count = proc_count - (proc_idx + 1)
        for neighbor_idx in xrange(1, missing_conn_count + 1):
          (end0, end1) = Pipe(True)
          proc_conns[proc_idx].append(end0)
          proc_conns[proc_idx + neighbor_idx].append(end1)
      # Bootstrap all the child processes.
      for proc_idx in xrange(1, proc_count):
        name = "jobber-%s" % proc_idx
        target = ActorSystem(
          name, proc_conns[proc_idx], max_msgs_slice, max_time_slice, ip, port
        )
        proc = Process(name=name, target=target.start)
        proc.start()
    # Bootstrap this process and have it join the other processes.
    connections = None
    if proc_conns is not None:
      connections = proc_conns[0]
    actor_system = ActorSystem(
      "jobber-0", connections, max_msgs_slice, max_time_slice, ip, port
    )
    actor_system.start()
    return actor_system

  def create(self, fqn, *args, **kwargs):
    # Load object.
    # Validate that it's an actor and implements receive and receive is callable.
    # Create actor reference

    # NOTE: This is typically bad and should make your linter complain.
    # Monkey patch the actor.
    #self._actor.actor_ref = actor_ref
    #self._actor.actor_system = self
    
    # Create actor processor
    # Start the actor processor
    # Return the actor reference.
    pass

  def find_global(self, fqn):
    pass

  def find_local(self, fqn):
    pass

  def start(self):
    #print self._name
    #print self._connections
    pass

  def shutdown(self):
    pass
