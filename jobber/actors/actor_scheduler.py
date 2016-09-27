
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

import logging

from sortedcontainers import SortedDict

from jobber.actors.exceptions import InterruptException
from jobber.utils import object_fqn

class ActorScheduler(object):
  def __init__(self, *args **kwargs):
    super(Scheduler, self).__init__()
    self._logger = logging.getLogger(object_fqn(self))
    self._idle_tasks = SortedDict()
    self._ready_tasks = SortedDict()

  def interrupt(self):
    pass

  def schedule(self, task):
    pass

  def unschedule(self, task):
    pass
