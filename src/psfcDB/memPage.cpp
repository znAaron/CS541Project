#include "memPage.h"

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <queue>

MemPage::MemPage(uint64_t index) {
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
int MemPage::addNode(const Node *node) {
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

MemPage *MemPage::splitPage() {
    std::sort(h_data, h_data + PAGE_SIZE, compareNodes);
    size = PAGE_SIZE / 2;

    uint64_t nextIndex = h_data[size].zIndex;

    // cout << "nextIndex: " << nextIndex << endl;

    MemPage *nextPage = new MemPage(nextIndex);
    memcpy(nextPage->h_data, &h_data[size], sizeof(Node) * size);
    nextPage->size = PAGE_SIZE / 2;

    // add to the list
    nextPage->prev = this;
    nextPage->next = next;
    next = nextPage;

    flush();
    nextPage->flush();

    return nextPage;
}

void MemPage::printPage() {
    cout << "Page " << startIndex << endl;
    for (int i = 0; i < size; i++) {
        cout << h_data[i].zIndex << " ";
    }
    cout << endl;
}

void MemPage::flush() {
    cudaMemcpy(d_data, h_data, PAGE_SIZE * sizeof(Node), cudaMemcpyHostToDevice);
}
