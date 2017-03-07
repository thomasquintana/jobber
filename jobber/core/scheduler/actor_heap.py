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

import heapq as heap
from jobber.core.scheduler.runtime_dict import RuntimeDict

from jobber.core.exceptions.no_messages_exception import NoMessagesException

class ShortestJobNextHeap(object):
    """
    Implements Shortest Job Next logic as a heap.
    Provides the Interface of a list.
    """
    def __init__(self):
        self._heap = list()
        self.message_statistics = RuntimeDict()

    def insert(self, actor_processor):
        """
        Inserts an actor into the heap
        """
        actor_processor.set_message_statistics(self.message_statistics)
        heap.heappush(self._heap, actor_processor)

    def first(self):
        try:
            return self._heap[0]
        except IndexError:
            raise NoMessagesException

    def pop(self):
        first = self.first()
        if first.pending_message_count == 0:
            heap.heapreplace(self._heap, first)
            raise NoMessagesException
        elif first.completed():
            self.remove(first)

        message = first.pop_message()
        heap.heapreplace(self._heap, first)
        return (first, message)

    def remove(self, processor):
        self._heap.remove(processor)
        heap.heapify(self._heap)

    def __len__(self):
        return len(self._heap)

    def __getitem__(self, index):
        return self._heap[index]
