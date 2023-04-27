#include <cuda_runtime.h>
#include <memPage.h>
#include <node.h>

#include <cstdint>
#include <iostream>
#include <map>
#include <queue>

class PsfcIndex {
   private:
    std::queue<MemPage*> dirtyQueue;
    std::map<uint64_t, MemPage*> pageMap;  // RB tree to find the page
    MemPageList pageList;

    MemPage* findPage(const std::map<uint64_t, MemPage*>& pageMap, uint64_t zIndex) {
        auto it = pageMap.upper_bound(zIndex);
        if (it == pageMap.begin()) {
            return nullptr;
        }
        --it;
        return it->second;
    }

   public:
    PsfcIndex() {
        Node* dummyNode = new Node(0, 0, -MAX_LONG, -MAX_LAT, "placeholder");
        MemPage* firstPage = new MemPage(0);
        int added = firstPage->addNode(dummyNode);
        dirtyQueue.push(firstPage);
    }

    void addNode(Node* node) {
        MemPage* pageToInsert = findPage(pageMap, node->zIndex);
        if (pageToInsert == nullptr) {
            std::cerr << "Error finding the first page!" << std::endl;
        }
    }
};