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

from jobber.core.actor.mailbox import Mailbox

class MailboxTests(unittest.TestCase):
    def setUp(self):
        self.mailbox = Mailbox()
        self.test_message = 'some message'
        self.other_message = 'other message'

    def test_append(self):
        self.mailbox.append(self.test_message)
        self.assertTrue(self.mailbox._box[0] == self.test_message)

    def test_append_preserves_fifo(self):
        self.mailbox.append(self.test_message)
        self.mailbox.append(self.other_message)
        self.assertTrue(self.mailbox._box[0] == self.test_message)
        self.assertTrue(self.mailbox._box[1] == self.other_message)

    def test_first(self):
        self.mailbox.append(self.test_message)
        self.mailbox.append(self.other_message)
        first_message = self.mailbox.first()
        self.assertTrue(first_message == self.test_message)

    def test_pop_from_empty_raises_indexerror(self):
        with self.assertRaises(IndexError):
            self.mailbox.pop()

    def test_pop_returns_element(self):
        self.mailbox.append(self.test_message)
        popped_element = self.mailbox.pop()
        self.assertTrue(popped_element == self.test_message)

    def test_pop_returns_first_element(self):
        self.mailbox.append(self.test_message)
        self.mailbox.append(self.other_message)
        popped_element = self.mailbox.pop()
        self.assertTrue(popped_element == self.test_message)

    def test_len(self):
        length = len(self.mailbox)
        self.assertTrue(length == 0)

    def test_len_returns_length(self):
        self.mailbox.append(self.test_message)
        length = len(self.mailbox)
        self.assertTrue(length == 1)

    def test_flush_empty(self):
        self.mailbox.flush()
        self.assertTrue(len(self.mailbox) == 0)

    def test_flush(self):
        for _ in range(50):
            self.mailbox.append(self.test_message)
            self.mailbox.append(self.other_message)
        self.mailbox.flush()
        self.assertTrue(len(self.mailbox) == 0)
