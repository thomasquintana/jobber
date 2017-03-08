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

AVERAGE = 'average'
CALLS = 'calls'

class RuntimeDict(object):
    """
    Efficiently stores and updates message runtimes
    """
    def __init__(self):
        self._runtimes = {}

    def get(self, _type):
        if not _type in self._runtimes:
            self._insert(_type)
        return self._runtimes[_type][AVERAGE]

    def update(self, _type, runtime):
        if not _type in self._runtimes:
            self._insert(_type)

        record = self._runtimes[_type]
        new_average = (record[AVERAGE]*record[CALLS] + runtime)/(record[CALLS]+1)
        record[AVERAGE] = new_average
        record[CALLS] += 1

    def _insert(self, _type):
        self._runtimes[_type] = {AVERAGE: 0.0, CALLS: 0}
