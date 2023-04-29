#ifndef MEMPAGELIST_H
#define MEMPAGELIST_H

#include "memPage.h"

class MemPageList {
   private:
    MemPage* h_head;
    MemPage* h_tail;

   public:
    MemPageList();
    void appendPage(MemPage* node);
    MemPage* head();
    void printList();
};

#endif