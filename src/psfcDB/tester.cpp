#include <chrono>

#include "index.h"

void populateNodes(PsfcIndex* index, int numNodes) {
    for (int i = 0; i < numNodes; i++) {
        Node* node = generateRandomNode();
        index->addNode(node);
    }
    for (int i = 0; i < numNodes; i++) {
        Node* node = generateRandomNamedNode();
        index->addNode(node);
    }
    cout << "Num of pages after population: " << index->numPages() << endl;
    // index->printIndex();
}

bool testFindNodesHost(PsfcIndex* index) {
    auto start = chrono::high_resolution_clock::now();
    int count = index->findNodes_Host(make_tuple(MAX_LAT, -MAX_LONG),
                                      make_tuple(-MAX_LAT + 1, MAX_LONG - 1));
    auto end = chrono::high_resolution_clock::now();
    // Calculate the duration
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start).count();
    cout << "Execution time: " << duration << " microseconds" << endl;

    cout << count << endl;
    return true;
}

bool testFindNodesDevice(PsfcIndex* index) {
    auto start = chrono::high_resolution_clock::now();
    int count = index->findNodes_device(make_tuple(MAX_LAT, -MAX_LONG),
                                        make_tuple(-MAX_LAT + 1, MAX_LONG - 1));
    auto end = chrono::high_resolution_clock::now();
    // Calculate the duration
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start).count();
    cout << "Execution time: " << duration << " microseconds" << endl;

    cout << count << endl;
    return true;
}

bool testFindNodesHostNamed(PsfcIndex* index) {
    auto start = chrono::high_resolution_clock::now();
    vector<Node*> nodes = index->findNodesNamed_Host(make_tuple(MAX_LAT, -MAX_LONG),
                                                     make_tuple(-MAX_LAT + 1, MAX_LONG - 1), "bob");
    auto end = chrono::high_resolution_clock::now();
    // Calculate the duration
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start).count();
    cout << "Named Execution time: " << duration << " microseconds" << endl;

    cout << nodes.size() << endl;
    return true;
}

int main() {
    PsfcIndex* index = new PsfcIndex();
    populateNodes(index, PAGE_SIZE * SM_NUM * 200);
    index->flushAll();

    testFindNodesHost(index);
    testFindNodesDevice(index);
}