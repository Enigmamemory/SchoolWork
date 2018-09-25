#ifndef SPINLOCK_H
#define SPINLOCK_H

#include <stdio.h>

struct spinlock{

  char taslock;
  
};

int tas(volatile char *lock);

void spin_lock(struct spinlock *l);

void spin_unlock(struct spinlock *l);

#endif
