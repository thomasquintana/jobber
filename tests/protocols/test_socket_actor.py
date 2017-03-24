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

import unittest
from mock import create_autospec, Mock, patch
import socket

from jobber.core.actor.actor import Actor
from jobber.protocols.socket_actor import (ClientSocketActor,
        ScheduleSendAllMessage, ScheduleReceiveUntilEmptyMessage)

TEST_HOSTNAME = 'testhostname'
TEST_PORT = 123456

class ClientSocketActorTest(unittest.TestCase):
    def setUp(self):
        self.tcp_socket_actor = ClientSocketActor.tcp()
        self.actor = Mock(Actor)

    def test_connect(self):
        with patch('socket.socket'):
            self.tcp_socket_actor = ClientSocketActor.tcp()
            self.tcp_socket_actor.connect(TEST_HOSTNAME, TEST_PORT)

            self.tcp_socket_actor.socket.connect.assert_called_with((TEST_HOSTNAME, TEST_PORT))
            self.tcp_socket_actor.socket.setblocking.assert_called_with(0)

    def test_close(self):
        with patch('socket.socket'):
            self.tcp_socket_actor = ClientSocketActor.tcp()
            self.tcp_socket_actor.close()

            self.tcp_socket_actor.socket.shutdown.assert_called_with(1)
            self.tcp_socket_actor.socket.close.assert_called_with()

    def test_socket_send_empty_payload(self):
        payload = ''
        self.assertTrue(payload == self.tcp_socket_actor._socket_send(payload))

    def test_socket_send(self):
        with patch('socket.socket'):
            self.tcp_socket_actor = ClientSocketActor.tcp()

            payload = 'some string'
            new_payload = self.tcp_socket_actor._socket_send(payload)
            self.tcp_socket_actor.socket.send.assert_called_with(payload)

    def test_socket_receive(self):
        with patch('socket.socket'):
            self.tcp_socket_actor = ClientSocketActor.tcp()

            self.tcp_socket_actor._socket_receive()
            self.tcp_socket_actor.socket.recv.assert_called_once()

    def test_send_all_empty_payload(self):
        payload = ''

        self.tcp_socket_actor.send_all(payload, self.actor)
        self.actor.tell.assert_called_once()

    def test_send_all(self):
        payload = 'some string'

        self.tcp_socket_actor.tell = Mock()
        self.tcp_socket_actor.send_all(payload, self.actor)

        self.tcp_socket_actor.tell.assert_called_once()

    def test_receive_until_empty_error(self):

        self.tcp_socket_actor.tell = Mock()
        self.tcp_socket_actor.receive_until_empty('some string', self.actor)

        self.tcp_socket_actor.tell.assert_called_once()

    def test_receive_until_empty(self):
        with patch('socket.socket'):
            self.tcp_socket_actor = ClientSocketActor.tcp()

        self.tcp_socket_actor.tell = Mock()
        self.tcp_socket_actor.receive_until_empty('some string', self.actor)
        self.tcp_socket_actor.tell.assert_called_once()
