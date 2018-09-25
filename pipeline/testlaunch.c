#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char** argv[]){

  int pipe1[2];

  pid_t wordgen,wordsearch,pager;

  pipe(pipe1);
  
  switch(wordgen=fork()) {
    
  case -1:
    fprintf(stderr, "wordgen fork failed");
    break;
    
  case 0:

    close(pipe1[0]);
    
    if (dup2(pipe1[1],1)<0){
      perror("Can't dup2 pipe1[1] to stdout");
      return -1;
    }

    if (argc == 1) 
      execl("/home/engine/Desktop/OS/wordgen","wordgen",(char *)NULL); 
    else 
      execl("/home/engine/Desktop/OS/wordgen","wordgen",argv[1],(char *)NULL);
    
    break;

  default: {

    close(pipe1[1]);

    int pipe2[2];
    pipe(pipe2);
    
    switch(wordsearch=fork()) {

    case -1:
      fprintf(stderr, "wordsearch fork failed");
      break;
      
    case 0:

      close(pipe2[0]);

      if (dup2(pipe1[0],0)<0){
	perror("Can't dup2 pipe1[0] to stdin");
	return -1;
      }

      if (dup2(pipe2[1],1)<0){
	perror("Can't dup2 pipe2[1] to stdout");
	return -1;
      }

      execl("/home/engine/Desktop/OS/wordsearch","wordsearch","wordlist_small.txt",(char *)NULL);

      break;

    default:{

      close(pipe1[0]);
      close(pipe2[1]);

      switch(pager=fork()){

      case -1:
	fprintf(stderr, "pager fork failed");
	break;

      case 0:

	if (dup2(pipe2[0],0)<0){
	  perror("Can't dup2 pipe2[0] to stdin");
	  return -1;
	}

	execl("/home/engine/Desktop/OS/pager","pager","pager",(char *)NULL);

	break;

      default: {

	close(pipe2[0]);
	
	int status,status2,status3;
	pid_t wpid,wpid2,wpid3;
	
	if ((wpid = wait(&status)) != -1) 
	  fprintf(stderr,"Child %i exited with %i\n",wpid,status);
	else
	  perror("First Wait Failed");
	
	if((wpid2 = wait(&status2)) != -1)
	  fprintf(stderr,"Child %i exited with %i\n",wpid2,status2);
	else
	  perror("Second Wait Failed");

	if((wpid3 = wait(&status3)) != -1)
	  fprintf(stderr,"Child %i exited with %i\n",wpid3,status3);
	else
	  perror("Third Wait Failed");

	break;
      }
	
      }
      
    }
      
    }

    break;
  }
    
  }

  return 0;

}
