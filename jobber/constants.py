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

JOBBER_PORT         = 5555
JOBBER_SCHEME       = 'jobber'
LOCAL_HOST          = '127.0.0.1'

# Actor processor states.
ACTOR_PROCESSOR_COMPLETED = 'Completed'
ACTOR_PROCESSOR_IDLE      = 'Idle'
ACTOR_PROCESSOR_READY     = 'Ready'
ACTOR_PROCESSOR_RUNNING   = 'Running'

# Actor scheduler states.
ACTOR_SCHEDULER_RUNNING  = 'Running'
ACTOR_SCHEDULER_STOPPED  = 'Stopped'
ACTOR_SCHEDULER_STOPPING = 'Stopping'

# Time periods expressed in milliseconds.
MS_SECOND = int(1000)
MS_MINUTE = int(60 * MS_SECOND)
MS_HOUR   = int(60 * MS_MINUTE)
MS_DAY    = int(24 * MS_HOUR)
MS_WEEK   = int(7  * MS_DAY)
