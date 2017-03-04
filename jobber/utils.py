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

from jobber.constants import MS_WEEK, MS_DAY, MS_HOUR, MS_MINUTE, MS_SECOND

def format_ms(ms):
    """
    Returns a formatted string for a period of time in milliseconds.

    Positional Arguments:
    period -- the period of time in milliseconds to be formatted.
    """

    result = ''
    if ms >= MS_WEEK:
        result += '{} week(s) '.format(ms / MS_WEEL)
        ms = ms % MS_WEEK

    if ms >= MS_DAY:
        result += '{} day(s) '.format(ms / MS_DAY)
        ms = ms % MS_DAY

    if ms >= MS_HOUR:
        result += '{} hour(s) '.format(ms / MS_HOUR)
        ms = ms % MS_HOUR

    if ms >= MS_MINUTE:
        result += '{} minute(s) '.format(ms / MS_MINUTE)
        ms = ms % MS_MINUTE

    if ms >= MS_SECOND:
        result += '{} second(s) '.format(ms / MS_SECOND)
        ms = ms % MS_SECOND

    if ms > 0:
        result += '{} millisecond(s)'.format(ms)
    else:
        result = result[:-1]
        
    return result

def object_fqn(o):
    """
    Return the fully qualified name of an object.

    Positional arguments:
    o -- the object.
    """

    return "{}.{}".format(o.__class__.__module__, o.__class__.__name__)

def time_delta_ms(start_time, end_time):
    """
    Returns a time delta between a start time and end time in milliseconds.

    Positional arguments:
    start_time -- the start time.
    end_time   -- the end time.
    """

    return int((end_time - start_time) * MS_SECOND)

def time_to_ms(time):
    """
    Convert the output of time.time to milliseconds.

    Positional arguments:
    time -- the input time.
    """

    return int(time * MS_SECOND)
