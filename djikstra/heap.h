#ifndef _HEAP_H
#define _HEAP_H

#include <vector>
#include <string>

#include "hash.h"

class heap {

 public:

  heap(int capacity);

  int getNodeFilled();

  void setNodeFilled(int filler);

  int getNodeNum();

  void setNodeNum(int filler);

  int MinKey();
  
  int insert(const std::string &id, long int key, void *pv = NULL);

  int setKey(const std::string &id, long int key);

  int deleteMin(std::string *pId = NULL, long int *pKey = NULL, void **ppData = NULL);

  int remove(const std::string &id, long int *pKey = NULL, void **ppData = NULL);

 private:
  
  class node{
  public:
    std::string id;
    long int key;
    void *pData = NULL;
  };

  std::vector<node> data;
  hashTable *mapping;

  int nodenum;
  int nodefilled;
  
  void percolateUp(int posCur);

  void percolateDown(int posCur);
  
  int getPos(node *pn);
};

#endif //_HEAP_H
