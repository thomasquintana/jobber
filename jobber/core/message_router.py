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

from urlparse import urlparse

from jobber.constants import JOBBER_SCHEME
from jobber.core.actor import Actor

class MessageRouter(Actor):
  def __init__(self, name, ip, port, local_conns):
    super(MessageRouter, self).__init__()
    self._local_name = name
    self._local_ip = ip
    self._local_port = port
    self._local_conns = local_conns
    self._local_conns_lookup = None

  def on_start(self):
    local_conns = self._local_conns
    name = self._local_name
    ip = self._local_ip
    port = self._local_port
    if local_conns is not None and len(local_conns) > 0:
      # Generate our address and broadcast it to the other local processes.
      if ip is not None and len(ip) > 0 and \
         port is not None and name is not None and \
         len(name) > 0:
        url = urlparse("{}://{}:{}/{}".format(JOBBER_SCHEME, ip, port, name))
        for connection in local_conns:
          connection.send(url)
      # Create a lookup table of addresses to the other local processes.
      lookup_table = dict()
      for idx, connection in enumerate(local_conns):
        url = connection.recv()
        key = url.path[1:]
        lookup_table.update({key: idx})
        print name, idx, connection
      self._local_conns_lookup = lookup_table
    print self._local_conns_lookup

  def on_stop(self):
    pass
