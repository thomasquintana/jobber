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
import socket
from jobber.core.actor.actor import Actor

class ClientSocketActor(Actor):
    def __init__(self, target_hostname, target_port):
        super(SocketActor, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target_hostname = target_hostname,
        self.target_port = target_port

    def connect(self):
        self.socket.connect((self.target_hostname, self.target_port))
        self.socket.setblocking(0)

    def close(self):
        self.socket.shutdown(1)
        self.socket.close()

    def socket_send(self, payload):
        done = True
        if len(payload):
            done = False
            try:
                sent = self.socket.send(payload)
            except socket.error:
                # socket was not ready
                sent = 0
            remaining_payload = payload[sent:]

        return remaining_payload, done

    def socket_receive(self):
        try:
            received = self.socket.recv()
            error = False
        except socket.error:
            # socket was not ready
            received = ''
            error = True

        if len(received) or error:
            self.tell(SocketReceiveMessage())

        return received, error
