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

class ActorRef(object):
  '''
  
  Positional Arguments:
  mailbox   -- A reference to the referenced actor's mailbox.
  path      -- A valid url path to the referenced actor.
  uuid      -- A universally unique identifier for the referenced actor.
  '''

  def __init__(self, mailbox, path, uuid):
    super(ActorRef, self).__init__()
    self._mailbox = mailbox
    self._path = path
    self._urn = uuid

  def __getattr__(self, name):
    if name == "path":
      return self._path.geturl()
    elif name == "urn":
      return self._urn

  def tell(self, message):
    self._mailbox.append(message)
