dijkstra.exe: dijkstra.o graph.o heap.o hash.o
	g++ -o dijkstra.exe dijkstra.o graph.o heap.o hash.o -std=c++11

dijkstra.o: dijkstra.cpp
	g++ -c dijkstra.cpp -std=c++11

graph.o: graph.cpp graph.h
	g++ -c graph.cpp -std=c++11

heap.o: heap.cpp heap.h
	g++ -c heap.cpp -std=c++11

hash.o: hash.cpp hash.h
	g++ -c hash.cpp -std=c++11
