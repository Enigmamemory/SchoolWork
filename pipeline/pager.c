#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(){

  char* wordentry = malloc(sizeof(char)*15);
  size_t entrysize = 15;
  int ctr = 0;
  char* entrybuf = malloc(sizeof(char)*5);
  size_t bufsize = 5;
  while(getline(&wordentry,&entrysize,stdin) != -1){

    fwrite(wordentry,sizeof(char),strlen(wordentry),stdout);
    ctr++;
    
    if (ctr >= 23){
 
      printf("Press RETURN for more or Q to quit\n");
      FILE * startterm = fopen("/dev/tty","r");
      while(getline(&entrybuf,&bufsize,startterm) != -1){
	
	if(strcmp("q\n",entrybuf) == 0 || strcmp("Q\n",entrybuf) == 0){
	  fprintf(stderr,"TERMINATED BY Q COMMAND\n");
	  exit(0);
	}
	else{
	  ctr = 0;
	  break;
	}

      }
      
    }
  }
  
  return 0;
  
}
