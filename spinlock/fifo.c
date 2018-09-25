#include "fifo.h"
#include <stdlib.h>
#include <stdio.h>

void fifo_init(struct fifo *f) {

  f->next_write = 0;
  f->next_read = 0;
  f->filled = 0;
  spin_unlock(&f->ffmutex);
  cv_init(&f->full_cv);
  cv_init(&f->empty_cv);
  
}

void fifo_wr(struct fifo *f, unsigned long d) {

  /*Critical Region Here*/
  spin_lock(&f->ffmutex);
  while (f->filled >= MYFIFO_BUFSIZ)
    //write sleeps until filled goes back down
    cv_wait(&f->full_cv,&f->ffmutex);
  f->buf[f->next_write] = d;
  f->next_write++;
  f->next_write %= MYFIFO_BUFSIZ;
  f->filled++;
  cv_signal(&f->empty_cv);
  spin_unlock(&f->ffmutex);
  /*End of Critica Region*/
  
}

unsigned long fifo_rd(struct fifo *f) {

  /*Critical Region Here*/
  spin_lock(&f->ffmutex);
  unsigned long read_val;
  while(f->filled <= 0) //shouldn't ever be less than 0
    //read sleeps until filled goes up
    cv_wait(&f->empty_cv,&f->ffmutex);
  read_val = f->buf[f->next_read];
  f->next_read++;
  f->next_read %= MYFIFO_BUFSIZ;
  f->filled--;
  cv_signal(&f->full_cv);
  spin_unlock(&f->ffmutex);
  /*End of Critical Region*/
  
  return read_val;
  
}

/*
int main() {
  return 0;
}
*/
