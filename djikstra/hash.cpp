#include <cstdlib>
#include "hash.h"
#include <vector>
#include <string>
#include <iostream>
#include <fstream>

using namespace std;

//Public Functions

hashTable::hashTable(int size) {
  //capacity = size;
  capacity = getPrime(size);
  filled = 0;
  data.resize(capacity);
}

int hashTable::getCap() { //test function
  return capacity;
}

int hashTable::getdataSize() { //test function 2
  return data.size();
}

void hashTable::printVector() {
  for(int ct = 0; ct < data.size(); ct++){
    cout << "inserted: " << data[ct].key << endl;
  }
}

int hashTable::getFill(){
  return filled;
}

int hashTable::insert(const string &key, void *pv){

  //ofstream ofs ("result.txt");
  //cout << "pv at hash insert: " << pv << endl;
  
  if (filled*2 > capacity){
    if (!rehash())
      return 2;
  }

  bool wrapped = false;
  unsigned int posi = hash(key);
  int orig = posi;
  
  while (!wrapped || (posi != orig)){
    
    //cout << "index of posi: " << posi << endl;
    //cout << "actual key: " << key << endl;
    //cout << "data[posi] occupied?: " << data[posi].isOccupied << endl;
    if (data[posi].isOccupied){
      //cout << "data[posi]: " << data[posi].key << endl;
      if (data[posi].key == key && !data[posi].isDeleted)
	return 1;
      if(posi < data.size()){
	//cout << "posi before add: " << posi << endl;
	posi++;
	//cout << "posi after add: " << posi << endl;
      }
      else{
	posi = 0;
	wrapped = true;
      }
    }
    else{
      data[posi].key = key;
      data[posi].isOccupied = true;
      data[posi].isDeleted = false;
      //if (pv != NULL)
      data[posi].pv = pv;
      //cout << "data[posi].pv at hash insert: " << data[posi].pv << endl;
      filled++;
      //cout << "inserted at " << posi << ": " << key << endl;
      //cout << posi << ": " << key << endl;
      //ofs << posi << ": " << key << endl;
      return 0;
    }
  }

  //ofs.close();
  
  cout << "Somehow wrapped around without rehash error, very bad" << endl;
    
  return 2;
  
}

bool hashTable::contains(const string &key){
  //cout << "key: " << key;
  if (findPos(key) != -1)
    return true;
  else
    return false;
}

void* hashTable::getPointer(const string &key, bool *b){
  int posi = findPos(key);
  if (posi != -1){
    if (b != NULL)
      *b = true;
    return data[posi].pv;
  }
  else {
    if (b != NULL)
      *b = false;
    return NULL;
  }
}

int hashTable::setPointer(const string &key, void *pv){
  int posi = findPos(key);
  if (posi != -1){
    data[posi].pv = pv;
    return 0;
  }
  else{
    //cout << endl << "we ended up here somehow" << endl;
    return 1;
  }
}

bool hashTable::remove(const string &key){
  int posi = findPos(key);
  if (posi != -1){
    data[posi].isDeleted = true;
    return true;
  } 
  else
    return false;
}

//Private Functions

int hashTable::hash(const string &key){ //using DJB2, needs to be tested

  unsigned int hash = 5381;
  int c;

  for (int i =0; i< key.length(); ++i) {
    c = (int) key[i];
    hash = ((hash << 5) + hash) + c;
    
  }
  int testing = hash % (capacity - 1);
  //cout << "hash modded: " << testing << endl;
  return testing;
  
}

int hashTable::findPos(const string &key){

  bool wrapped = false;
  unsigned int posi = hash(key);
  int orig = posi;

  //ofstream ofs ("result.txt");
  
  while (!wrapped || (posi != orig)){
    
    //cout << "index of posi: " << posi << endl;
    //cout << "actual key: " << key << endl;
    //cout << "data[posi] occupied?: " << data[posi].isOccupied << endl;
    if (data[posi].isOccupied){
      //cout << "data[posi]: " << data[posi].key << endl;
      if (data[posi].key == key && data[posi].isDeleted == false)
	return posi;
      if(posi < data.size()){
	//cout << "posi before add: " << posi << endl;
	posi++;
	//cout << "posi after add: " << posi << endl;
      }
      else{
	posi = 0;
	wrapped = true;
      }
    }
    else{
      return -1;
      /*
      data[posi].key = key;
      data[posi].isOccupied = true;
      filled++;
      //cout << "inserted at " << posi << ": " << key << endl;
      //cout << posi << ": " << key << endl;
      //ofs << posi << ": " << key << endl;
      return 0;
      */
    }
  }

  return -1;

  //ofs.close();

  
  /*
  int pos = -1;
  //int fpos = 0;
  
  for(vector<hashItem>::iterator it = data.begin(); it != data.end(); it++){
    if (key == (*it).key)
      return pos = it - data.begin();
    //fpos++;
    //missing return value for when the hash is empty?
  }
  

  return pos;
  */
}

bool hashTable::rehash(){
  //ofstream ofs ("result.txt");
  int size = getPrime(capacity+1);
  //ofs << "\nrehashing here\n" << endl;
  //cout << "prime before rehash: " << capacity << endl;
  //cout << "filled slots: " << filled << endl;
  //ofs.close();
  if (size == -1)
    return false;
  else{
    hashTable temp(capacity + 1);
    //cout << "prime of temp: " << temp.capacity << endl << endl;
    for (int ct = 0; ct < data.size(); ct++){
      if (data[ct].isOccupied == true && data[ct].isDeleted == false)
	temp.insert(data[ct].key,data[ct].pv);
    }
    //cout << "filled in temp: " << temp.filled << endl;
    data = temp.data;
    capacity = size;
    return true;
  }
}

unsigned int hashTable::getPrime(int size){
  int primes[] = {24593, 49157, 98317, 196613, 393241, 786433, 1572689, 3145739};
  int cprimes = 0;
  for (; cprimes < sizeof(primes)/sizeof(primes[0]); cprimes++) {

    if (size < primes[cprimes]){
      size = primes[cprimes];
      break;
    }
    
  }
  if (cprimes >= sizeof(primes)/sizeof(primes[0]))
    return -1;
  return size;
    
}
