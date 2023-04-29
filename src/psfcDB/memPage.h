#ifndef MEMPAGE_H
#define MEMPAGE_H

#include <cuda_runtime.h>

#include <cstdint>
#include <cstring>

#include "node.h"

using namespace std;

#define PAGE_SIZE 1024

struct MemPage {
    int size;
    int capacity;
    uint64_t startIndex;  // the smallest index in this page
    MemPage *prev;
    MemPage *next;

    Node *h_data;
    Node *d_data;
    bool dirty;

    MemPage(uint64_t index);
    int addNode(const Node *node);
    MemPage *splitPage();
    void flush();
    void printPage();
};

#endif