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

import socket, thread

from jobber.core.actor import Actor
from jobber.core.messages.datagram import Datagram

class MessageRouter(Actor):
  def __init__(self, name, ip, port, local_conns, gateway=False):
    super(MessageRouter, self).__init__()
    self._local_name = name
    self._local_ip = ip
    self._local_port = port
    self._local_conns = local_conns
    self._local_conns_lookup = None
    self._local_gateway_idx = None
    self._gateway = gateway
    self._udp_sock = None

  def on_datagram(self, message):
    destination = message.destination
    if destination.hostname == self._local_ip and \
       destination.port == self._local_port:
      # Handle messages destined for our host.
      tokens = destination.path[1:].split("/")
      if tokens[0] == self._local_name:
        # Handle messages destined for our process.
        actor_ref = self.actor_system.find_local(".".join(tokens[1:-1]))
        if actor_ref is not None:
          actor_ref.tell(message)
      else:
        # Handle messages destined for a different process.
        conn = self._local_conns[self._local_conns_lookup[tokens[0]]]
        conn.send(message)
    else:
      # Handle messages destined for other hosts.
      if not self._gateway:
        # Use a gateway.
        gateway_idx = self._local_gateway_idx
        if gateway_idx is not None:
          gateway = self._local_conns[gateway_idx]
          gateway.send(message)
      else:
        # Send the message to another host or actor system via UDP.
        self._udp_sock.sendto(message, (self._local_ip, self._local_port))

  def on_start(self):
    # Bootstrap the local connections.
    conns = self._local_conns
    if conns is not None and len(conns) > 0:
      # Broadcast our identity to the other processes.
      for connection in conns:
        connection.send((self._local_name, self._gateway))
      # Create a lookup table to the other processes.
      lookup_table = dict()
      for idx, connection in enumerate(conns):
        name, gateway = connection.recv()
        lookup_table.update({name: idx})
        if gateway:
          self._local_gateway_idx = idx
      self._local_conns_lookup = lookup_table
    # Setup the public interface.
    if self._gateway:
      self._udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self._udp_sock.bind((self._local_ip, self._local_port))

  def on_stop(self):
    if self._gateway:
      self._udp_sock.close()

  def receive(self, message):
    '''
    This method processes incoming messages.
    '''

    if isinstance(message, Datagram):
      self.on_datagram(message)
