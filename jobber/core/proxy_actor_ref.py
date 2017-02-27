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

import socket

class LocalProxyActorRef(object):
  '''
  
  Positional Arguments:
  mailbox   -- A reference to the referenced actor's mailbox.
  url       -- A valid url to the referenced actor.
  uuid      -- A universally unique identifier for the referenced actor.
  '''

  def __init__(self, mailbox, router, url, uuid):
    super(LocalProxyActorRef, self).__init__()
    self._url = url
    self._urn = uuid

  @property
  def url(self):
    return self._url

  def tell(self, message):
    pass

  @property
  def urn(self):
    return self._urn

class RemoteProxyActorRef(object):
  '''
  
  Positional Arguments:
  mailbox   -- A reference to the referenced actor's mailbox.
  url       -- A valid url to the referenced actor.
  uuid      -- A universally unique identifier for the referenced actor.
  '''

  def __init__(self, mailbox, router, url, uuid):
    super(RemoteProxyActorRef, self).__init__()
    self._url = url
    self._urn = uuid

  @property
  def url(self):
    return self._url

  def tell(self, message):
    pass

  @property
  def urn(self):
    return self._urn
