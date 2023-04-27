#include <memPage.h>

#include <cstdint>
#include <iostream>
#include <queue>

class MemPageList {
   private:
    MemPage *h_head;
    MemPage *h_tail;

    void addPage(const MemPage &page) {
        MemPage *node = new MemPage(page);
        if (h_head == nullptr) {
            h_head = node;
            h_tail = node;
        } else {
            h_tail->next = node;
            node->prev = h_tail;
            h_tail = node;
        }
    }

    void removePage(const MemPage *page) {
        if (page == nullptr) {
            return;
        }
        if (page == h_head) {
            h_head = page->next;
        }
        if (page == h_tail) {
            h_tail = page->prev;
        }
        if (page->prev != nullptr) {
            page->prev->next = page->next;
        }
        if (page->next != nullptr) {
            page->next->prev = page->prev;
        }
        delete page;
    }

   public:
    MemPageList() {
        h_head = nullptr;
        h_tail = nullptr;
    }
};