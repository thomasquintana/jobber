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

from jobber.errors import GREEN_THREAD_INV_NAME_TYPE, \
                          GREEN_THREAD_INV_PRIORITY_TYPE, \
                          GREEN_THREAD_INV_PREV_PROC_TIME_TYPE, \
                          GREEN_THREAD_INV_TOTAL_PROC_TIME_TYPE

class Task(object):
  '''
  A task is a lightweight thread of execution.
  '''

  def __init__(self, name=None, priority=10):
    super(Task, self).__init__()
    self._name = name or self.__class__.__name__
    self._priority = priority
    self._prev_proc_time = 0.
    self._total_proc_time = 0.

  def __getattr__(self, name):
    if name == "name":
      return self._name
    elif name == "priority":
      return self._priority
    elif name == "prev_proc_time":
      return self._prev_proc_time
    elif name == "total_proc_time":
      return self._total_proc_time

  def __setattr__(self, name, value):
    if name == "name":
      self._name = value
    elif name == "priority":
      self._priority = value
    elif name == "prev_proc_time":
      self._prev_proc_time = value
    elif name == "total_proc_time":
      self._total_proc_time = value
    else:
      super(Task, self).__setattr__(name, value)

  def execute(self):
    '''
    This method will be scheduled for execution by the scheduler..
    '''

    pass
