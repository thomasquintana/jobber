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

BUFFER_SIZE = 2**11

class ClientSocketActor(Actor):
    def __init__(self, client_socket):
        super(ClientSocketActor, self).__init__()
        self.socket = client_socket

    @classmethod
    def udp(cls):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return cls(_socket)

    @classmethod
    def tcp(cls):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return cls(_socket)

    def connect(self, target_hostname, target_port):
        self.socket.connect((target_hostname, target_port))
        self.socket.setblocking(0)

    def close(self):
        self.socket.shutdown(1)
        self.socket.close()

    def _socket_send(self, payload):
        remaining_payload = payload

        if len(payload):
            try:
                sent = self.socket.send(payload)
            except socket.error:
                # socket was not ready
                sent = 0
            remaining_payload = payload[sent:]

        return remaining_payload

    def _socket_receive(self):
        try:
            received = self.socket.recv(BUFFER_SIZE)
            error = False
        except socket.error as e:
            # socket was not ready
            received = ''
            error = True

        return received, error

    def send_all(self, payload, actor):
        """
            sends the entire payload
            once done, sends message to actor
        """
        remaining_payload = self._socket_send(payload)
        print remaining_payload
        if remaining_payload:
            self.tell(ScheduleSendAllMessage(remaining_payload, actor))
        else:
            actor.tell(SocketSendDone())

    def receive_until_empty(self, existing_payload, actor):
        """
            receives until an empty response is received from socket
            once done, sends message to actor
        """
        received, error = self._socket_receive()

        if received == '' and not error:
            actor.tell(SocketReceiveDone(existing_payload))
        else:
            self.tell(ScheduleReceiveUntilEmptyMessage(existing_payload+received, actor))

    def receive(self, message):
        if isinstance(message, ScheduleSendAllMessage):
            self.send_all(message.get_payload(), message.get_actor())
        elif isinstance(message, ScheduleReceiveUntilEmptyMessage):
            self.receive_until_empty(self, existing_payload, actor)


class SocketSendDone(object):
    pass

class SocketReceiveDone(object):
    def __init__(self, payload):
        self._payload = payload

    def get_payload():
        return self._payload

class ScheduleSendAllMessage(object):
    def __init__(self, payload, actor):
        self._payload = payload
        self._actor = actor

    def get_payload():
        return self._payload

    def get_actor():
        return self._actor

class ScheduleReceiveUntilEmptyMessage(object):
    def __init__(self, payload, actor):
        self._payload = payload
        self._actor = actor

    def get_payload():
        return self._payload

    def get_actor():
        return self._actor
