import logging
import time

from threading import Event

from sortedcontainers import SortedListWithKey

from jobber.core.exceptions.interrupt_exception import InterruptException
from jobber.core.exceptions.scheduler_stopped_exception import SchedulerStoppedException
from jobber.constants import (ACTOR_PROCESSOR_COMPLETED, ACTOR_SCHEDULER_RUNNING,
        ACTOR_SCHEDULER_STOPPED, ACTOR_SCHEDULER_STOPPING)

from jobber.utils import object_fully_qualified_name

class Scheduler(object):
    """
    Scheduler Interface
    """

    def __init__(self, slice_msgs):
        super(ActorScheduler, self).__init__()
        self._logger = logging.getLogger(object_fully_qualified_name(self))
        self._state = ACTOR_SCHEDULER_STOPPED
        self._processors = list()

    def _run(self):
        """
        Implements the scheduling function
        """
        pass

    def schedule(self, actor_proc):
        if self._state == ACTOR_SCHEDULER_RUNNING:
            self._procs.add((0., actor_proc))
            self._barrier.set()
        else:
            raise SchedulerStoppedException

    def shutdown(self):
        if self._state == ACTOR_SCHEDULER_RUNNING:
            for _, proc in self._procs:
                proc.stop_gracefully()

            self._state = ACTOR_SCHEDULER_STOPPING

    def shutdown_now(self):
        self._state = ACTOR_SCHEDULER_STOPPED

    def start(self):
        if self._state == ACTOR_SCHEDULER_STOPPED:
            self._state = ACTOR_SCHEDULER_RUNNING
            self._run()
