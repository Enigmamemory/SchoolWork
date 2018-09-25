#include "hash.h"
#include "heap.h"

#include <cstdlib>
#include <vector>
#include <string>
#include <iostream>

using namespace std;

heap::heap(int capacity){

  data.resize(capacity+1);
  mapping = new hashTable(capacity*2);
  nodenum = capacity;
  nodefilled = 0;
  
}

int heap::getNodeFilled(){
  return nodefilled;
}

void heap::setNodeFilled(int filler){
  nodefilled = filler;
}

int heap::getNodeNum(){
  return nodenum;
}

void heap::setNodeNum(int filler){
  nodenum = filler;
}

int heap::MinKey(){
  return data[1].key;
}

int heap::insert(const string &id, long int key, void *pv){
  //nodenum = getNodeNum();
  //nodefilled = getNodeFilled();
  
  if (nodenum == nodefilled){
    return 1;
  }

  //cout << "id of insert: " << id << endl;
  //cout << "pv of insert: " << pv << endl;
  bool contained = mapping->contains(id);
  //cout << "contained: " << contained << endl;
  if (contained)
    return 2;
  else{
    nodefilled++;
    data[nodefilled].id = id;
    data[nodefilled].key = key;
    //if (pv != NULL)
    data[nodefilled].pData = pv;
    //cout << "id in heap insert is: " << id << endl;
    //cout << "pv in heap insert is: " << pv << endl;
    mapping->insert(id,(void *)&data[nodefilled]);
    percolateUp(nodefilled);
    return 0;
  }
  
}

int heap::setKey(const string &id, long int key){
  if (mapping->contains(id)){
    int up;
    node* nodeadd = (node *)mapping->getPointer(id);
    int pos = getPos(nodeadd);
    if (min(data[pos].key,key) == key)
      up = 1;
    else
      up = 0;
    data[pos].key = key;
    if (up == 1)
      percolateUp(pos);
    else
      percolateDown(pos);
    return 0;
  }
  else
    return 1;
}

int heap::deleteMin(string *pId, long int *pKey, void **ppData){
  string remember = data[1].id;
  //cout << "id at deleteMin is: " << remember << endl;
  if(remove(data[1].id,pKey,ppData) == 1)
    return 1;
  else{
    //cout << "are we here?" << endl;
    //cout << "remember is: " << remember << endl;
    *pId = remember;
    //cout << "assigned pointer to remember" << endl;
    return 0;
  }

}

int heap::remove(const string &id, long int *pKey, void **ppData){
  

  if (mapping->contains(id)){
    int up;
    node* noderem = (node *)mapping->getPointer(id);
    //cout << "noderem: " << noderem << endl;
    int pos = getPos(noderem);

    if (pKey != NULL){
      //cout << "pKey: " << pKey << endl;
      //cout << "pos: " << pos << endl;
      //cout << "data[pos].key: " << data[pos].key << endl;
      *pKey = data[pos].key;
    }

    //cout << "before ppData if statement" << endl;
    if (ppData != NULL){
      *ppData = (void *)data[pos].pData;
      //cout << "ppData at remove/deleteMin is: " << ppData << endl;
      //cout << "*ppData is: " << *ppData << endl;
    }
    //cout << "after ppData if statement" << endl;
    
    if (min(data[pos].key,data[nodefilled].key) == data[nodefilled].key)
      up = 1;
    else
      up = 0;
    //cout << "after determining up variable" << endl;
    //cout << "up: " << up << endl;
    int check1 = mapping->setPointer(data[nodefilled].id, (void *)noderem);
    //cout << "segfault here?" << endl;
    bool checkrem = mapping->remove(id);
    //cout << "data[pos].id: " << data[pos].id << endl;
    //cout << "data[pos].key: " << data[pos].key << endl;
    data[pos] = data[nodefilled];
    //cout << "data[pos].id after: " << data[pos].id << endl;
    //cout << "data[pos].key after: " << data[pos].key << endl;
    nodefilled--;
    if (pos > nodefilled)
      return 0;
    if (up == 1)
      percolateUp(pos);
    else
      percolateDown(pos);
    return 0;
  }
  else
    return 1;
}

void heap::percolateUp(int posCur){
  if (posCur > 1) {
    int ogkey = data[posCur].key;
    int upkey = data[posCur/2].key;
    if (ogkey < upkey){
      //cout << "something happened in percUp" << endl;
      void *ptr1 = mapping->getPointer(data[posCur].id);
      void *ptr2 = mapping->getPointer(data[posCur/2].id);
      //cout << "ptr2: " << ptr2 << endl;
      //cout << "posCur/2: " << posCur/2 << endl;
      //cout << "data[posCur/2].id: " << data[posCur/2].id << endl;
      int check1 = mapping->setPointer(data[posCur].id, ptr2);
      int check2 = mapping->setPointer(data[posCur/2].id, ptr1);
      if (check1 == 0 && check2 == 0){
	swap(data[posCur],data[posCur/2]);
	if (posCur/2 > 1)
	  percolateUp(posCur/2);
      }
      else
	cout << "setPointer encountered issues. check1: " << check1 << ", check2: " << check2 << endl;
      
    }
  }
}

void heap::percolateDown(int posCur){
  //cout << "Reached PercolateDown" << endl;
  if (posCur*2 <= nodefilled){
    int compkey;
    int ogkey = data[posCur].key;
    int d1key = data[posCur*2].key;
    int d2key;
    //cout << "Reached decision tree in percolatedown" << endl;
    if (posCur*2 + 1 <= nodefilled){
      //cout << "well I'm wrong" << endl;
      //cout << "wtf is posCur*2 + 1: " << posCur*2 + 1 << endl;
      d2key = data[posCur*2 + 1].key;
      compkey = min(d1key,d2key);
      //cout << "it ran fine here" << endl;
    }
    else{
      //cout << "I think we're here" << endl;
      compkey = d1key;
    }
    //cout << "before ogkey > compkey" << endl;
    if (ogkey > compkey){
      //cout << "so that means ogkey > compkey" << endl;
      void *ptr1 = mapping->getPointer(data[posCur].id);
      void *ptr2;
      int check2;
      if (compkey == d2key && posCur*2 + 1 <= nodefilled){
	ptr2 = mapping->getPointer(data[posCur*2 + 1].id);
        check2 = mapping->setPointer(data[posCur*2 + 1].id,ptr1);
      }
      else{
	ptr2 = mapping->getPointer(data[posCur*2].id);
	check2 = mapping->setPointer(data[posCur*2].id,ptr1);
      }
      int check1 = mapping->setPointer(data[posCur].id, ptr2);
      if (check1 == 0 && check2 == 0){
	if (compkey == d2key && posCur*2 + 1 <= nodefilled){
	  swap(data[posCur], data[posCur*2 + 1]);
	  if (posCur*2 + 1 <= nodefilled)
	    percolateDown(posCur*2 + 1);
	}
	else{
	  swap(data[posCur], data[posCur*2]);
	  if (posCur*2 <= nodefilled)
	    percolateDown(posCur*2);
	}
      }

    }
    //cout << "wait wtf we skipped everything?" << endl; 
  }

}

int heap::getPos(node *pn){
  //cout << "pn: " << pn << endl;
  //cout << "&data[0]: " << &data[0] << endl;
  int pos = pn - &data[0];
  return pos;
}
