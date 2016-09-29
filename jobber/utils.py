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

from jobber.constants import MS_DAY, MS_HOUR, \
                             MS_MINUTE, MS_SECOND, MS_WEEK

def format_ms(ms):
  '''
  Returns a formatted string for a period of time in milliseconds.

  Positional Arguments:
  period -- the period of time in milliseconds to be formatted.
  '''

  result = ""
  temp = None
  if ms >= MS_WEEK:
    temp = ms / MS_WEEK
    result += "%i weeks " % temp
    ms -= temp * MS_WEEK
  if ms >= MS_DAY:
    temp = ms / MS_DAY
    result += "%i days " % temp
    ms -= temp * MS_DAY
  if ms >= MS_HOUR:
    temp = ms / MS_HOUR
    result += "%i hours " % temp
    ms -= temp * MS_HOUR
  if ms >= MS_MINUTE:
    temp = ms / MS_MINUTE
    result += "%i minutes " % temp
    ms -= temp * MS_MINUTE
  if ms >= MS_SECOND:
    temp = ms / MS_SECOND
    result += "%i seconds " % temp
    ms -= temp * MS_SECOND
  result += "%i milliseconds" % ms
  return result

def object_fqn(o):
  '''
  Return the fully qualified name of an object.

  Positional arguments:
  o -- the object.
  '''

  return "%s.%s" % (o.__class__.__module__, o.__class__.__name__)

def time_delta_ms(start_time, end_time):
  '''
  Returns a time delta between a start time and end time in milliseconds.
  
  Positional arguments:
  start_time -- the start time.
  end_time   -- the end time.
  '''

  return int((end_time - start_time) * 1e3)
