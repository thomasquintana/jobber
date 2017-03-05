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

import heapq
from jobber.core.scheduler.runtime_dict import RuntimeDict

class ShortestJobNextHeap(object):
    """
    Implements Shortest Job Next logic as a heap.
    Provides the Interface of a list.
    """
    def __init__(self):
        self._heap = list()
        self.message_statistics = RuntimeDict()

    def insert(self, actor_processor):
        actor_processor.set_message_statistics(self.message_statistics)
        heapq.heappush(self._heap, actor_processor)

    def first(self):
        return self._heap[0]
