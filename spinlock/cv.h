#ifndef CV_H
#define CV_H

#include "spinlock.h"

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

#define CV_MAXPROC 64

struct cv {

  struct spinlock *call_mutex;
  struct spinlock cvmutex;
  int sleepers[CV_MAXPROC];
  int numsleep;

};

void cv_init(struct cv *cv);

void cv_wait(struct cv *cv, struct spinlock *mutex);

int cv_broadcast(struct cv *cv);

int cv_signal(struct cv *cv);

#endif
