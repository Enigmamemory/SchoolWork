#include "hash.h"
#include "heap.h"
#include "graph.h"

#include <cstdlib>
#include <vector>
#include <string>
#include <iostream>
#include <map>
#include <fstream>

using namespace std;

graph::graph() {
  newnodes = new hashTable(50);
  //dist(10^9 + 1);
}

graph::node::node(){
  dist = 1000000001;
}

int graph::InsertNewNode(const string &id){ //returns -1 if already exists, returns 1 for insert success
  /*
  if (!newnodes->contains(id)){
    nodenum++;
    nodename.resize(nodenum);//try push_back?
    nodename[nodenum-1] = id;
    //cout << "checking if insert worked: " << nodedata[nodenum].id << endl;
    //cout << "checking nodenum: " << nodenum << endl;
    newnodes->insert(id,(void *)&nodedata[nodenum]);
    return 1;
  }
  else
    return -1;
  */
  if (!newnodes->contains(id)){
    nodenum++;
    nodename.resize(nodenum);
    nodename[nodenum-1] = id;
    /*
    nodedata[id];
    cout << "Testing nodedata[id].dist: " << nodedata[id].dist << endl;
    nodedata[id].dist = 10^9 + 1;
    cout << "Testing nodedata[id].dist after edit: " <<  nodedata[id].dist << endl;
    */

    node testing;
    //cout << "testing.dist at InsertNewNode before edits: " << testing->dist << endl;
    testing.id = id;
    //testing-> dist = 0;
    //cout << "testing.dist after edits" << testing.dist << endl;
    nodedata.insert(pair<string,node>(id,testing));
    /*
    
    testing.id = id;
    testing.known = false;
    testing.dist = 10^9 + 1;
    testing.path = NULL;
    cout << "testing.dist at InsertNewNode: " << testing.dist << endl;
    cout << "testing.id at InsertNewNode: " << testing.id << endl;
    //nodedata.insert(pair<string,node>(id,*testing));
    */
    //cout << "node with id " << id << " submitted pointer value: " << &nodedata[id] << endl;
    newnodes->insert(id,(void *)&nodedata[id]);
    //cout << "did pointer value change?" << &nodedata[id] << endl;
    //cout << "what did I enter into hashtable? " << newnodes->getPointer(id) << endl;
    return 1;
  }
  else
    return -1;
}

int graph::InsertAdjEdges(const string &id, const string &idadj, int dist){//see inseert
  //cout << "Beginning of InsertAdjEdges" << endl;
  if(newnodes->contains(id)){
    //int vectpos = SetPos(id);
    //cout << "vectpos: " << vectpos << endl;
    nodedata[id].adjedge.insert(pair<string,int>(idadj,dist));
    return 1;
  }
  else
    return -1;
}

int graph::CheckNodeInserted(const string &id){
  return newnodes->contains(id);
}

int graph::SetDist(const string &id, int newdist, void *path){//return 2 for change, 1 for no change, -1 for fail
  if(newnodes->contains(id)){
    //cout << "contain check in SetDist clear" << endl;
    //cout << "value of nodedata[id].dist " << nodedata[id]->dist << endl;
    //cout << "value of newdist " << newdist << endl;
    //node* startnode = (node *)newnodes->getPointer(id);
    //int vectpos = startnode - &nodedata[0];
    if (nodedata[id].dist > newdist){
      //cout << "Made it to compare if statement" << endl;
      nodedata[id].dist = newdist;
      nodedata[id].path = (node *)path;
      startdist->setKey(id,newdist);
      return 2;
    }
    else //these may not be necessary
      return 1;
  }
  else
    return -1;
}

int graph::NodeInsertHeap(){
  /*
  for (int vectct = 0; vectct < nodedata.size(); vectct++){
    string id = nodedata[vectct].id;
    startdist->insert(id,nodedata[vectct].dist,newnodes->getPointer(id));
  }
  */
  ChangeHeapSize();
  for (map<string,node>::iterator it = nodedata.begin(); it != nodedata.end(); ++it){
    string id = it->second.id;
    //cout << "id in NodeInsertHeap: " << id << endl;
    startdist->insert(id,it->second.dist,newnodes->getPointer(id));
    //cout << "node with id " << id << " has pointer: " << newnodes->getPointer(id) << endl;
  }
  return 1;
}

int graph::DjikstraLoop(){//return 1 to terminate loop, return 0 to indicate it should keep going

  //cout << "Reached Loop" << endl;
  if (knownnum == nodenum){
    //cout << "known = node num" << endl;
    return 1;
  }
  long int minkey = startdist->MinKey();
  //cout << "What is minkey? " << minkey << endl << endl;
  if (minkey == 1000000001){
    //cout << "minkey = 10^9 + 1" << endl;
    return 1;
  }
  //cout << "Passed if statements in loop" << endl;
  string *holdId = new string;
  void **holdptr = new void*; //might be something diff
  startdist->deleteMin(holdId,NULL,holdptr);
  //cout << "Passed deletemin" << endl;
  //cout << "at loop, node with id " << *holdId << " has holdptr: " << holdptr << endl;
  //cout << "*holdptr is: " << *holdptr << endl;
  SetKnown(*holdId);

  //int vectPos = SetPos(*holdId);
  /*
  if (!nodedata[vectPos].adjedge.empty()){
    int curdist = nodedata[vectPos].dist;
    for (map<string,int>::iterator it = nodedata[vectPos].adjedge.begin(); it != nodedata[vectPos].adjedge.end(); it++)
      {
	string adjid = it->first;
	int adjdist = it->second;
	
	if(CompDist(adjid,adjdist+curdist)){
	  SetDist(adjid,adjdist+curdist,holdptr);
	}
	
      }
  }
  */
  node curnode = nodedata[*holdId];
  if (!curnode.adjedge.empty()){
    int curdist = curnode.dist;
    for (map<string,int>::iterator it = curnode.adjedge.begin(); it != curnode.adjedge.end(); it++){
      string adjid = it->first;
      int adjdist = it->second;
      
      if(CompDist(adjid,adjdist+curdist)){
	SetDist(adjid,adjdist+curdist,*holdptr);
      }
    }
  }
  
  return 0;
  
}

void graph::ChangeHashSize(int size){

}

int graph::OutputGraph(string filename){
  
  ofstream outfile(filename);

  if(!outfile.is_open()) {
    cout << "Output file didn't open for some reason" << endl;
    return -1;
  }
  else {
    //cout << "Well, I mean, I guess I should've seen this coming, yes" << endl;
    //for(int vectct = 1; vectct < nodedata.size(); vectct++){
    //for(map<string,node>::iterator it=nodedata.begin(); it!=nodedata.end(); ++it) {
    for (int namect = 0; namect < nodename.size(); namect++) {

      string nodeid = nodename[namect];
      node curnode = nodedata[nodeid];
      //string curnode = it->second.id;
      outfile << nodeid << ": ";

      //cout << "Current node id: " << curnode << endl;
      //cout << "Address of current node: " << &nodedata[curnode] << endl;
      //cout << "Current node path: " << it->second.path << endl;
      //if (it->second.path != NULL)
      //cout << "Current node path's id: " << it->second.path->id << endl;
      
      if (curnode.dist >= 1000000001 && curnode.path == NULL)
	outfile << "NO PATH" << endl;

      else{
	int curdist = curnode.dist;
	outfile << curdist << " [";

	node *curpath = curnode.path;
	vector<string> pathnodes;
	while (curpath != NULL){
	  vector<string>::iterator it2 = pathnodes.begin();
	  pathnodes.insert(it2, curpath->id);
	  curpath = curpath->path;
	}
	if (pathnodes.size() != 0) {
	  for (int pathct = 0; pathct < pathnodes.size(); pathct++){
	    outfile << pathnodes[pathct] << ", ";
	  }
	}
	outfile << nodeid << "]" << endl;
      }
    }
    
    outfile.close();
    return 1;
  }
  
}

int graph::NodeKnown(const string &id){
  if(newnodes->contains(id)){
    //int vectpos = SetPos(id);
    return nodedata[id].known;
  }
  else
    return -1;
}

int graph::SetKnown(const string &id){
  if(newnodes->contains(id)){
    //int vectpos = SetPos(id);
    nodedata[id].known = true;
    knownnum++;
    return 1;
  }
  else
    return -1;
}

void graph::CheckAdjEdges(const string &id){
  
}

int graph::CompDist(const string &id,int newdist){ //return 1 if need replace, -1 for error
  if (newnodes->contains(id)){
    //int vectpos = SetPos(id);
    if (nodedata[id].dist > newdist)
      return 1;
    else
      return 0;
  }
  else
    return -1;
}

void graph::ChangeHeapSize(){
  startdist = new heap(nodenum+1);
}

/*
int graph::SetPos(const string &id){
  node* startnode = (node *)newnodes->getPointer(id);
  int pos = startnode - &nodedata[0];
  return pos;
}
*/
