#include "spinlock.h"

#include <stdio.h>
#include <errno.h>
#include <sched.h>

void spin_lock(struct spinlock *l){

  //fprintf(stderr,"l->taslock is %s\n",l->taslock);
  
  //tas(&l->taslock);
  while(tas(&l->taslock) != 0)
    sched_yield();
  
}

void spin_unlock(struct spinlock *l){

  //volatile char *lock = l->taslock;
  
  //if (tas(&l->taslock) != 0)
  l->taslock = 0;
  
}

/*
int main() {
  return 0;
}
*/
