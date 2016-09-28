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

import math

from jobber.constants import DAY_MU_SECONDS, HOUR_MU_SECONDS, \
                             MINUTE_MU_SECONDS, MU_SECOND, WEEK_MU_SECONDS

def format_time_period(period):
  '''
  Returns a formatted string describing a time period.

  Note: Intel + 64bit Linux report back in microsecond granularity for calls
        to time.clock() and time.time().

  Positional Arguments:
  period -- the period of time in microseconds to be formatted.
  '''

  result = ""
  temp = None
  if period >= WEEK_MU_SECONDS:
    temp = int(math.floor(period / WEEK_MU_SECONDS))
    result += "%i weeks " % temp
    period -= temp * WEEK_MU_SECONDS
  if period >= DAY_MU_SECONDS:
    temp = int(math.floor(period / DAY_MU_SECONDS))
    result += "%i days " % temp
    period -= temp * DAY_MU_SECONDS
  if period >= HOUR_MU_SECONDS:
    temp = int(math.floor(period / HOUR_MU_SECONDS))
    result += "%i hours " % temp
    period -= temp * HOUR_MU_SECONDS
  if period >= MINUTE_MU_SECONDS:
    temp = int(math.floor(period / MINUTE_MU_SECONDS))
    result += "%i minutes " % temp
    period -= temp * MINUTE_MU_SECONDS
  if period >= MU_SECOND:
    temp = int(math.floor(period / MU_SECOND))
    result += "%i seconds " % temp
    period -= temp * MU_SECOND
  if period >= 1000:
    temp = int(math.floor(period / 1000))
    result += "%i milliseconds " % temp
    period -= temp * 1000
  result += "%i microseconds" % period
  return result

def object_fqn(o):
  '''
  Return the fully qualified name of an object.

  Positional arguments:
  o -- the object.
  '''

  return "%s.%s" % (o.__class__.__module__, o.__class__.__name__)
