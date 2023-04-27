#ifndef MEMPAGE_H
#define MEMPAGE_H

#include <cuda_runtime.h>
#include <node.h>

#include <cstdint>
#include <cstring>

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

    MemPage(uint64_t index) {
        size = 0;
        capacity = PAGE_SIZE;
        startIndex = index;
        prev = nullptr;
        next = nullptr;

        cudaMallocHost((Node **)&h_data, PAGE_SIZE * sizeof(Node));
        cudaMalloc((Node **)&d_data, PAGE_SIZE * sizeof(Node));
        dirty = false;
    }

    // return 1 if becomes dirty, 0 if success, -1 if failed
    int addNode(const Node *node) {
        if (size >= capacity) {
            return -1;
        }

        h_data[size] = *node;
        size++;

        int result = 0;
        if (!dirty) {
            result = 1;
            dirty = true;
        }

        return result;
    }
};

class MemPageList {
   public:
    MemPageList();
};
#endif