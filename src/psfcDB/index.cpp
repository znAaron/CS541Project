#include "index.h"

#include <cuda_runtime.h>

PsfcIndex::PsfcIndex() {
    Node* dummyNode = new Node(0, 0, -MAX_LAT, -MAX_LONG, "placeholder");
    MemPage* firstPage = new MemPage(0);
    firstPage->addNode(dummyNode);
    pageList.appendPage(firstPage);
    pageMap[firstPage->startIndex] = firstPage;
    dirtyPages.insert(firstPage);
}

MemPage* PsfcIndex::findPage(const map<uint64_t, MemPage*>& pageMap, uint64_t zIndex) {
    auto it = pageMap.upper_bound(zIndex);
    if (it == pageMap.begin()) {
        return nullptr;
    }
    --it;
    return it->second;
}

void PsfcIndex::addNode(Node* node) {
    // cout << "before adding Adding node " << node->zIndex << endl;
    // printIndex();

    MemPage* pageToInsert = findPage(pageMap, node->zIndex);
    if (pageToInsert == nullptr) {
        cerr << "Error finding the first page!" << endl;
    }

    int nodeAdded = pageToInsert->addNode(node);
    if (nodeAdded < 0) {
        // cout << "Splitting page" << endl;
        MemPage* nextPage = pageToInsert->splitPage();
        if (dirtyPages.count(pageToInsert) > 0) {
            dirtyPages.erase(pageToInsert);
        }

        pageMap[nextPage->startIndex] = nextPage;

        if (node->zIndex < nextPage->startIndex) {
            pageToInsert->addNode(node);
            dirtyPages.insert(pageToInsert);
        } else {
            nextPage->addNode(node);
            dirtyPages.insert(nextPage);
        }
    } else if (nodeAdded == 1) {
        dirtyPages.insert(pageToInsert);
    }

    // cout << "after adding Adding node " << node->zIndex << endl;
    // printIndex();
    // cout << "##################################################" << endl;
}

// count the nodes in the corners
// corner if defined as <lat, long>
vector<Node*> PsfcIndex::findNodes_Host(tuple<double, double> topLeft,
                                        tuple<double, double> bottomRight) {
    vector<Node*> result;

    uint64_t start = coordToZIndex(get<0>(topLeft), get<1>(topLeft));
    uint64_t finish = coordToZIndex(get<0>(bottomRight), get<1>(bottomRight));

    int pageVisted = 0;
    MemPage* currPage = findPage(pageMap, start);
    while (currPage != nullptr && currPage->startIndex <= finish) {
        for (int i = 0; i < currPage->size; i++) {
            Node* currNode = &currPage->h_data[i];
            if (currNode->zIndex > finish) {
                break;
            }

            if (currNode->inRegion(topLeft, bottomRight)) {
                result.push_back(currNode);
            }
        }

        currPage = currPage->next;
        pageVisted++;
    }

    cout << "Pages visited: " << pageVisted << endl;
    return result;
}

vector<Node*> PsfcIndex::findNodesNamed_Host(tuple<double, double> topLeft,
                                             tuple<double, double> bottomRight, const char* name) {
    vector<Node*> result;

    uint64_t start = coordToZIndex(get<0>(topLeft), get<1>(topLeft));
    uint64_t finish = coordToZIndex(get<0>(bottomRight), get<1>(bottomRight));

    int pageVisted = 0;
    MemPage* currPage = findPage(pageMap, start);
    while (currPage != nullptr && currPage->startIndex <= finish) {
        // cout << "currPage->startIndex: " << currPage->startIndex << endl;

        for (int i = 0; i < currPage->size; i++) {
            Node* currNode = &currPage->h_data[i];
            if (currNode->zIndex > finish) {
                break;
            }

            if (currNode->inRegion(topLeft, bottomRight) && currNode->nameContains(name)) {
                result.push_back(currNode);
            }
        }
        currPage = currPage->next;
        pageVisted++;
    }

    cout << "Pages visited: " << pageVisted << endl;
    return result;
}

int PsfcIndex::numPages() { return pageMap.size(); }

void PsfcIndex::printIndex() {
    cout << "================== index ===================" << endl;
    pageList.printList();
}
