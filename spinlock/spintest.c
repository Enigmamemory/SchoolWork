#include "spinlock.c"

#include <sys/mman.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

struct spinlock *l;

int main(int argc, char** argv){

  //l = malloc(sizeof(*l));
  l = mmap(NULL, sizeof(*l), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0); 
  l->taslock = 0;
 
  int* addr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0); 
  int number;
  int cores;
  
  if (argc > 2){
    number = atoi(argv[1]);
    cores = atoi(argv[2]);
  }
  
  else {
    fprintf (stderr, "Need to enter a number of iterations and a number of cores\n");
    return -2;
  }

  pid_t child;

  for (int i = 0; i < 8 ; i++){

    switch(child=fork()){
    case -1:

      fprintf(stderr, "wordgen fork failed");
      return -1;
      
    case 0: {

      int testtas;
      //testtas = ;

      //fprintf(stderr, "value of testtas: %i\n",testtas);
      
      //Critical Region Starts Here
      //while (tas(&l->taslock) != 0) {
	//fprintf(stderr,"lock is working\n");
      //}
 
      //spin_lock(l);

      //fprintf(stderr, "value of l->taslock after spin_lock: %i\n", l->taslock);
      //fprintf(stderr, "value of tas: %i\n", tas(&l->taslock));
      
      for (int j = 0; j < number; j++) {
	(*addr)++;
      }
      //spin_unlock(l);

      //fprintf(stderr, "past unlocked\n");
      //Critical Region Ends Here

      return 0;

    }
      
    default: {
      
    }
    }    
  }

  for (int k = 0; k < 8 ; k++){
      int status;
      pid_t wpid;
      if ((wpid = wait(&status)) != -1) 
	fprintf(stderr,"Child %i exited with %i\n",wpid,status);
      else
	fprintf(stderr,"Wait Failed\n");
  }

  fprintf(stderr, "Value of 8 * number: %i\n", 8*number);
  fprintf(stderr, "Value of *addr: %i\n", *addr);
  
  if ((8 * number) == *addr)
    fprintf(stderr, "Numbers match\n");
  else
    fprintf(stderr, "Numbers don't match\n");
  
  return 0;
  
}
