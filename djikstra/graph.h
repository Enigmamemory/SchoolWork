#ifndef _GRAPH_H
#define _GRAPH_H

#include <vector>
#include <string>
#include <map>

#include "hash.h"
#include "heap.h"

class graph{

 public:

  graph();

  int InsertNewNode(const std::string &id);

  int InsertAdjEdges(const std::string &id, const std::string &idadj, int dist);

  int CheckNodeInserted(const std::string &id);

  int SetDist(const std::string &id, int newdist, void *path = NULL);

  int NodeInsertHeap();

  int DjikstraLoop();

  void ChangeHashSize(int size);

  int OutputGraph(const std::string filename);

 private:

  class node{
  public:
    node();
    std::string id;
    std::map<std::string, int> adjedge;
    bool known = false;
    long int dist;
    node * path = NULL;
  };

  //std::vector<node> nodedata;
  std::map<std::string,node> nodedata;
  std::vector<std::string> nodename;
  hashTable *newnodes;
  heap *startdist;
  int nodenum = 0;
  int knownnum = 0;

  int NodeKnown(const std::string &id);

  int SetKnown(const std::string &id);

  void CheckAdjEdges(const std::string &id);

  int CompDist(const std::string &id,int newdist);

  void ChangeHeapSize();
  
  //int SetPos(const std::string &id);
  
};

#endif //_GRAPH_H
