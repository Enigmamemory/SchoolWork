#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char** argv){
  
  int infinity;
  int wordtotal;
  
  if (argc == 1 || *argv[1] == '0')
    infinity = 1;
  else 
    wordtotal = atoi(argv[1]);
  int ctr = 0;
  srand(time(NULL));
  char word[7];

  while (ctr < wordtotal || infinity == 1){
    int wordsz = 3 + (rand() % 3);

    for (int i = 0; i < wordsz; i++){
      char randlet = 65 + (rand() % 26);
      word[i] = randlet;
    }
    word[wordsz]='\n';
    word[wordsz+1]='\0';

    fwrite(word,sizeof(char),strlen(word),stdout);
    
    ctr++;
  }

  fprintf(stderr, "Generated %i words\n", ctr);
  
  return 0;
}
