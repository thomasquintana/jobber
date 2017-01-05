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

import time

class Datagram(object):
  def __init__(self, source, destination, message):
    super(Datagram, self).__init__()
    self._source = source
    self._destination = destination
    self._message = message
    self._timestamp = time.time()

  @property
  def source(self):
    return self._source

  @property
  def destination(self):
    return self._destination

  @property
  def message(self):
    return self._message

  @property
  def timestamp(self):
    return self._timestamp
