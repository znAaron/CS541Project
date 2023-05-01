#ifndef INDEX_H
#define INDEX_H

#include <cstdint>
#include <iostream>
#include <map>
#include <queue>
#include <tuple>
#include <unordered_set>
#include <vector>

#include "memPage.h"
#include "memPageList.h"
#include "node.h"

using namespace std;

#define SM_NUM 60
#define BATCH_SIZE 240

class PsfcIndex {
   private:
    unordered_set<MemPage*> dirtyPages;
    map<uint64_t, MemPage*> pageMap;  // RB tree to find the page
    MemPageList pageList;

    MemPage* findPage(const map<uint64_t, MemPage*>& pageMap, uint64_t zIndex);

   public:
    PsfcIndex();  // constructor
    void addNode(Node* node);
    void flushAll();
    int findNodes_Host(tuple<double, double> topLeft, tuple<double, double> bottomRight);
    int findNodes_device(tuple<double, double> topLeft, tuple<double, double> bottomRight);
    vector<Node*> findNodesNamed_Host(tuple<double, double> topLeft,
                                      tuple<double, double> bottomRight, const char* name);
    int numPages();
    void printIndex();
};

#endif