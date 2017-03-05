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
from mock import create_autospec, Mock

from jobber.core.scheduler.actor_heap import ShortestJobNextHeap
from jobber.core.actor.processor import ActorProcessor
from jobber.core.actor.actor import Actor

class ShortestJobNextHeapTests(unittest.TestCase):
    def setUp(self):
        self.heap = ShortestJobNextHeap()
        self.actorprocessor = ActorProcessor(create_autospec(Actor))
        self.other_actorprocessor = ActorProcessor(create_autospec(Actor))

    def test_heap_insert(self):
        self.heap.insert(self.actorprocessor)
        self.heap.insert(self.other_actorprocessor)
        self.assertTrue(self.heap.first() == self.actorprocessor)
