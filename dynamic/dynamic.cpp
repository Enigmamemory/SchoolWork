#include <cstdlib>
#include <vector>
#include <string>
#include <stack>
#include <iostream>
#include <fstream>

using namespace std;

int filled[1001][1001];

int OutMatch(const string wa,const string wb, const string wc, const string filename){

  ofstream outfile(filename, ofstream::app);
  
  if(!outfile.is_open()) {
    cout << "Output file didn't open for some reason" << endl;
    return -1;
  }
  else {

    for (int f1 = 0; f1 < 1001 ; f1++)
      for(int f2 = 0; f2 < 1001 ; f2++)
	filled[f1][f2] = 0;
    
    int ta = 0;
    int tb = 0;
    int upch = 0;
    
    stack<int> possible;
    stack<int> upper;
    
    int wasz = wa.size();
    int wbsz = wb.size();

    //hashTable filled(1);
    
    vector<char> out(wasz+wbsz,'0');
    char inout;

    if ((wasz + wbsz) != wc.size()){
      cout << "Failure" << endl;
      outfile << "*** NOT A MERGE ***" << endl;
      return 0;
    }
    
    //cout << "first word size: " << wa.size() << endl;
    //cout << "second word size: " << wb.size() << endl;
    
    while(ta < wasz || tb < wbsz){
    
      /*
	cout << "letter of first word: " << wa[ta] << endl;
	cout << "letter of second word: " << wb[tb] << endl;
	cout << "letter of tested word: " << wc[ta+tb] << endl;
	cout << "ta = " << ta << endl;
	cout << "tb = " << tb << endl;
      */
      
      if (ta < wasz){
	
	if (wa[ta] == wc[ta+tb]){
	  
	  if(wa[ta] == wb[tb]){
	    //cout << "Split" << endl;
	    possible.push(tb+1);
	    //cout << "tb + 1 = " << tb+1 << endl;
	    possible.push(ta);
	    //cout << "ta = " << ta << endl;
	    upper.push(0);
	  
	    possible.push(tb);
	    //cout << "tb  = " << tb+1 << endl;
	    possible.push(ta+1);
	    //cout << "ta + 1 = " << ta << endl;
	    upper.push(1);
	  }
	  else{
	    //cout << "Advancing First Word" << endl;
	    possible.push(tb);
	    //cout << "tb  = " << tb+1 << endl;
	    possible.push(ta+1);
	    //cout << "ta + 1 = " << ta << endl;
	    upper.push(1);
	  }
	
	}
      
      }
    
      if (tb < wbsz){
      
	//cout << "wb[tb] == wc[ta+tb]? -> " << (wb[tb] == wc[ta+tb]) << endl; 
	if (wb[tb] != wa[ta]) {
	  if (wb[tb] == wc[ta+tb]) {
	    //cout << "Advancing Second Word" << endl;
	    possible.push(tb+1);
	    //cout << "tb + 1 = " << tb+1 << endl;
	    possible.push(ta);
	    //cout << "ta = " << ta << endl;
	    upper.push(0);
	  
	  }
	}
      
      }
    
      if (!possible.empty()){
	int filler = 1;
	
	while(filler == 1){
	  
	  if(!possible.empty()) {
	    
	    ta = possible.top();
	    //cout << "(" << ta << ",";
	    possible.pop();
	    tb = possible.top();
	    //cout << tb << ")" << endl;
	    possible.pop();
	    upch = upper.top();
	    upper.pop();

	    if(filled[ta][tb] == 0) {
	      filled[ta][tb] = 1;
	      filler = 0;
	    }
	    
	    /*
	    string coord = "(";
	    coord.append(to_string(ta));
	    coord.append(",");
	    coord.append(to_string(tb));
	    coord.append(")");
	    
	    if(!filled.contains(coord)){
	      filled.insert(coord);
	      filler = 0;
	    }
	    */
	    /*
	    else{
	      cout << coord << " already has been checked" << endl;
	    }
	    */
	    
	  }
	  else {
	    //cout << "Ran out of things to pop" << endl;
	    break;
	  }
	}

	if(upch == 1)
	  inout = toupper(wa[ta-1]);
	else
	  inout = wb[tb-1];
	
	out[ta+tb-1] = inout;
	
	if (ta >= wa.size() && tb >= wb.size()){
	  //cout << "Success" << endl;
	  for (int ct = 0 ; ct < wasz + wbsz ; ct++){
	    outfile << out[ct];
	    cout << out[ct];
	  }
	  outfile << endl;
	  cout << endl;
	  //match term here
	  break;
	}	
	
      }
      else {
	
	if (ta >= wa.size() && tb >= wb.size()){
	  //cout << "Success" << endl;
	  for (int ct = 0 ; ct < wasz + wbsz ; ct++){
	    outfile << out[ct];
	    cout << out[ct];
	  }
	  outfile << endl;
	  cout << endl;
	  break;
	  //match term here
	}
	else{
	  cout << "Failure" << endl;
	  outfile << "*** NOT A MERGE ***" << endl;
	  break;
	  //no match term here
	}
	
      }
    
    }

    //outfile << outputs.rdbuf();
    //cout << outputs.rdbuf();
    
    outfile.close();
    return 0;
  }
}

int main(){

  cout << "Please enter an input file name" << endl;
  string infilen;
  getline(cin, infilen);
  ifstream infile(infilen);
  cout << "Please enter an output file name" << endl;
  string outfilen;
  getline(cin, outfilen);

  ofstream outfile(outfilen);
  
  if(!outfile.is_open()) {
    cout << "Output file didn't open for some reason" << endl;
    return -1;
  }

  outfile.close();
  
  if (!infile.is_open()){
    cout << "Could not open " << infilen << endl;
    return -1;
  }
  else{

    string word1;
    string word2;
    string word3;
    
    while(getline(infile,word1)){

      if((getline(infile,word2)) && (getline(infile,word3))){

	//cout << "reached loop" << endl;
	OutMatch(word1,word2,word3,outfilen);

      }
      
    }

    infile.close();
    return 0;
  }

  
  
}
