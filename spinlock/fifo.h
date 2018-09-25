#ifndef FIFO_H
#define FIFO_H

#include "spinlock.h"
#include "cv.h"

#define MYFIFO_BUFSIZ 1024

struct fifo {
  unsigned long buf[MYFIFO_BUFSIZ];
  int next_write,next_read;
  int filled;
  struct cv full_cv,empty_cv;
  struct spinlock ffmutex;
};

void fifo_init(struct fifo *f);

void fifo_wr(struct fifo *f, unsigned long d);

unsigned long fifo_rd(struct fifo *f);

#endif
