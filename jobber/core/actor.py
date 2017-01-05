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

class Actor(object):
  '''
  An actor is the most basic unit of computation in an actor framework.
  '''

  def __init__(self):
    super(Actor, self).__init__()
    self._actor_ref = None
    self._actor_system = None

  @property
  def actor_ref(self):
    return self._actor_ref

  @actor_ref.setter
  def actor_ref(self, actor_ref):
    self._actor_ref = actor_ref

  @property
  def actor_system(self):
    return self._actor_system

  @actor_system.setter
  def actor_system(self, actor_system):
    self._actor_system = actor_system

  def receive(self, message):
    '''
    This method processes incoming messages.
    '''

    pass
