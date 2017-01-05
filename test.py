#/usr/bin/python

from jobber.core.actor_system import ActorSystem

if __name__ == "__main__":
  ActorSystem.bootstrap_system(proc_count=3)
