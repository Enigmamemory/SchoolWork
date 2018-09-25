#include "graph.h"

#include <cstdlib>
#include <vector>
#include <string>
#include <iostream>
#include <map>
#include <fstream>

using namespace std;

int main(){

  graph djikstra;
  
  cout << "Please enter a file name" << endl;
  string filename;
  getline(cin, filename);
  ifstream myfile(filename);
  //cout << "Reached before reading file" << endl;
  if (myfile){
    
    string vectinfo;
    
    while(getline(myfile,vectinfo)){
      string delim = " ";
      size_t lastpos = 0;
      size_t nextpos = 0;
      vector<string> vectlist;
      string token;
      while((nextpos = vectinfo.find(delim,lastpos)) != string::npos){
	string token = vectinfo.substr(lastpos,nextpos-lastpos);
	lastpos = nextpos+1;
	vectlist.push_back(token);
	size_t start = 0;
      }
      vectlist.push_back(vectinfo.substr(lastpos));

      djikstra.InsertNewNode(vectlist[0]);
      djikstra.InsertNewNode(vectlist[1]);
      int adjdist = stoi(vectlist[2]);
      //cout << "Current Stuff: " << vectlist[0] << ", " << vectlist[1] << ", " << adjdist << endl;
      djikstra.InsertAdjEdges(vectlist[0],vectlist[1],adjdist);
      
    }
  }
  else {
    cout << "This file cannot be opened. It may not exist, or there may be some other issue" << endl;
    return -1;
  }

  int startdone = 0;
  string startnode;

  while (startdone == 0){
    cout << "Please enter a starting node" << endl;
    getline(cin,startnode);
    if (!djikstra.CheckNodeInserted(startnode))
      cout << "This is not a recorded vertex, please enter something else" << endl;
    else{
      //cout << "Before NodeInsertHeap()" << endl;
      djikstra.NodeInsertHeap();
      //cout << "Before SetDist" << endl;
      int funccheck = djikstra.SetDist(startnode,0);
      //cout << "SetDist check: " << funccheck << endl;
      int stoploop = 0;
      while (stoploop != 1) { 
	stoploop = djikstra.DjikstraLoop();
	
      }

      string outfile;
      cout << "Please enter an output file" << endl;
      getline(cin,outfile);

      djikstra.OutputGraph(outfile);
      startdone = 1;
    }
  }
  
  
  //read file and put vertexes in
  //prompt id of starting vertex
  //find vertex
  //set up vertex (set dist to 0)
  //put all vertexes in heap with weight = dist
  //loop Djikstra
  //create output file (need a loop thru path)
  return 0;
}
