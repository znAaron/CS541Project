#include "memPageList.h"

#include <cstdint>
#include <iostream>
#include <queue>

MemPageList::MemPageList() {
    h_head = nullptr;
    h_tail = nullptr;
}

void MemPageList::appendPage(MemPage* node) {
    if (h_head == nullptr) {
        h_head = node;
        h_tail = node;
    } else {
        h_tail->next = node;
        node->prev = h_tail;
        h_tail = node;
    }
}

MemPage* MemPageList::head() { return h_head; }

void MemPageList::printList() {
    MemPage* cur = h_head;
    while (cur != nullptr) {
        cur->printPage();
        cur = cur->next;
    }
};

void MemPageList::flushAll() {
    MemPage* cur = h_head;
    while (cur != nullptr) {
        cur->flush();
        cur = cur->next;
    }
};