#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/signal.h>

#define capacity 393241

char* data[capacity];
int filled[capacity];

int matchnum = 0;

void handler (int signum) {
  fprintf(stderr,"Total Matched Words: %i\n",matchnum);
  signal(SIGPIPE,SIG_DFL);
  raise(SIGPIPE);
}

int hash(const char* key){

  unsigned int hash = 5381;
  int c;

  for (int i = 0;i < strlen(key); ++i){
    c = key[i];
    hash=((hash<<5) + hash) + c;
  }

  int testing = hash % (capacity - 1);
  return testing;
  
}

int findPos(const char* key) {


  char* newkey = malloc(sizeof(char)*10);
  strcpy(newkey,key);

  int wrapped = 0;
  unsigned int posi = hash(newkey);
  int orig = posi;
  
  while(wrapped == 0 || (posi != orig)) {

    if (filled[posi] == 1){
      if (strcmp(newkey,data[posi]) == 0)
	return posi;
      if (posi < capacity)
	posi++;
      else{
	posi = 0;
	wrapped = 1;
      }
      
    }
    else {
      return -1;
    }
  }

  return -1;
  
}

int insert(const char* key){
  
  char* cpykey = malloc(sizeof(char)*40);
  strcpy(cpykey,key);

  int wrapped = 0;
  unsigned int posi = hash(cpykey);
  int orig = posi;
  
  while(wrapped == 0 || (posi != orig)) {
    
    if (filled[posi] == 1){
      if (strcmp(cpykey,data[posi]) == 0)
	return 1;
      if (posi < capacity)
	posi++;
      else{
	posi = 0;
	wrapped = 1;
      }  
    }
    else{
      filled[posi] = 1;
      data[posi] = cpykey;
      return 0;
    }


    
  }

  return -1;
  
}

int main(int argc, char** argv){

 

  FILE * dictlist;
  if (argc >= 2)
    dictlist = fopen(argv[1], "r");
  else { 
    dictlist = fopen("wordlist_small.txt","r");
  }
  
  char* dictbuf = malloc(sizeof(char)*40);
  size_t bufsize = 40;

  
  while(getline(&dictbuf, &bufsize, dictlist) > 0){
    insert(dictbuf);
  }

  char* wordentry = malloc(sizeof(char)*10);
  size_t entrysize = 10;

  int checkget = 0;

  signal(SIGPIPE, handler);
  
  while((checkget = getline(&wordentry,&entrysize,stdin)) > 0){

    if (findPos(wordentry) != -1){
      fwrite(wordentry,sizeof(char),strlen(wordentry),stdout);
      matchnum++;
    }
  }
  
  fprintf(stderr,"Total Matched Words: %i\n",matchnum);
  
  return 0;
  
}

