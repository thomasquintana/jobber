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
from uuid import uuid4

from jobber.constants import JOBBER_PORT, LOCAL_HOST
from jobber.core.actor_scheduler import ActorScheduler
from jobber.core.message_router import MessageRouter
from jobber.errors import ACTOR_REF_INVALID_PATH, ACTOR_REF_INVALID_SCHEME, \
                          ACTOR_SYSTEM_INVALID_PROC_COUNT

class ActorSystem(object):
  def __init__(self, name, connections, max_msgs_slice, max_time_slice,
               ip, port, gateway):
    super(ActorSystem, self).__init__()
    self._connections = connections
    self._name = name
    self._router = MessageRouter(name, ip, port, connections, gateway=gateway)
    self._scheduler = ActorScheduler(max_msgs_slice, max_time_slice)
  
  @staticmethod
  def bootstrap_system(ip=LOCAL_HOST, port=JOBBER_PORT, max_msgs_slice=10, \
                       max_time_slice=50, proc_count=cpu_count()):
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
          name, proc_conns[proc_idx], max_msgs_slice, max_time_slice, ip, port,
          gateway=False
        )
        proc = Process(name=name, target=target.start)
        proc.start()
    # Bootstrap this process and have it join the other processes.
    connections = None
    if proc_conns is not None:
      connections = proc_conns[0]
    actor_system = ActorSystem(
      "jobber-0", connections, max_msgs_slice, max_time_slice, ip, port,
      gateway=True
    )
    actor_system.start()
    return actor_system

  def create(self, fqn, visibility="local", *args, **kwargs):
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
    '''
    Returns an actor proxy that will facilitate communications between a local
    and remote actor.
    '''
    pass

  def find_local(self, fqn):
    '''
    Returns an actor ref
    '''
    pass

  def start(self):
    self._router.on_start()
    #print self._name
    #print self._connections
    pass

  def shutdown(self):
    pass
