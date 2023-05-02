#include <cuda_runtime.h>

#include "device_launch_parameters.h"
#include "index.h"

// CUDA kernel to filter nodes within a given region
__global__ void filterNodes(Node** pages, int* numNodes, double topLatitude, double leftLongitude,
                            double bottomLatitude, double rightLongitude, bool* results) {
    if (threadIdx.x < numNodes[blockIdx.x]) {
        Node* page = pages[blockIdx.x];

        double latitude = page[threadIdx.x].latitude;
        bool latitudeInRange = latitude >= bottomLatitude && latitude <= topLatitude;

        double longitude = page[threadIdx.x].longitude;
        bool longitudeInRange = longitude >= leftLongitude && longitude <= rightLongitude;

        bool inRegion = latitudeInRange && longitudeInRange;

        if (inRegion) {
            results[blockIdx.x * blockDim.x + threadIdx.x] = true;
        } else {
            results[blockIdx.x * blockDim.x + threadIdx.x] = false;
        }
    }
}

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
    MemPage* pageToInsert = findPage(pageMap, node->zIndex);
    if (pageToInsert == nullptr) {
        cerr << "Error finding the first page!" << endl;
    }

    int nodeAdded = pageToInsert->addNode(node);
    if (nodeAdded < 0) {
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
}

void PsfcIndex::flushAll() { pageList.flushAll(); }

// count the nodes in the corners, corner if defined as <lat, long>
int PsfcIndex::findNodes_Host(tuple<double, double> topLeft, tuple<double, double> bottomRight) {
    int result = 0;

    uint64_t start = coordToZIndex(get<0>(topLeft), get<1>(topLeft));
    uint64_t finish = coordToZIndex(get<0>(bottomRight), get<1>(bottomRight));

    int pageVisted = 0;
    MemPage* currPage = findPage(pageMap, start);
    while (currPage != nullptr && currPage->startIndex <= finish) {
        for (int i = 0; i < currPage->size; i++) {
            Node* currNode = &currPage->h_data[i];
            // cout << currNode->to_string() << " ";

            if (currNode->inRegion(topLeft, bottomRight)) {
                result++;
            }
        }

        currPage = currPage->next;
        pageVisted++;
        // cout << endl;
    }

    return result;
}

// count the nodes in the corners, corner if defined as <lat, long>
int PsfcIndex::findNodes_device(tuple<double, double> topLeft, tuple<double, double> bottomRight) {
    int count = 0;

    double topLatitude = std::get<0>(topLeft);
    double leftLongitude = std::get<1>(topLeft);
    double bottomLatitude = std::get<0>(bottomRight);
    double rightLongitude = std::get<1>(bottomRight);

    uint64_t start = coordToZIndex(get<0>(topLeft), get<1>(topLeft));
    uint64_t finish = coordToZIndex(get<0>(bottomRight), get<1>(bottomRight));

    int pageVisted = 0;
    MemPage* currPage = findPage(pageMap, start);

    Node** h_pages;
    Node** d_pages;
    cudaMallocHost((Node***)&h_pages, BATCH_SIZE * sizeof(Node*));
    cudaMalloc((Node***)&d_pages, BATCH_SIZE * sizeof(Node*));

    int* h_numNodes;
    int* d_numNodes;
    cudaMallocHost((int**)&h_numNodes, BATCH_SIZE * sizeof(int));
    cudaMalloc((int**)&d_numNodes, BATCH_SIZE * sizeof(int));

    bool* d_results;
    cudaMalloc((bool**)&d_results, BATCH_SIZE * PAGE_SIZE * sizeof(bool));

    int pageCount = 0;
    while (currPage != nullptr && currPage->startIndex <= finish) {
        h_pages[pageCount] = currPage->d_data;
        h_numNodes[pageCount] = currPage->size;
        pageCount++;

        if (pageCount == BATCH_SIZE) {
            cudaMemcpy(d_pages, h_pages, BATCH_SIZE * sizeof(Node*), cudaMemcpyHostToDevice);
            cudaMemcpy(d_numNodes, h_numNodes, BATCH_SIZE * sizeof(int), cudaMemcpyHostToDevice);

            dim3 blockSize(PAGE_SIZE);
            dim3 gridSize(BATCH_SIZE);
            filterNodes<<<gridSize, blockSize>>>(d_pages, d_numNodes, topLatitude, leftLongitude,
                                                 bottomLatitude, rightLongitude, d_results);

            bool* results = new bool[BATCH_SIZE * PAGE_SIZE];

            cudaMemcpy(results, d_results, BATCH_SIZE * PAGE_SIZE * sizeof(bool),
                       cudaMemcpyDeviceToHost);

            for (int i = 0; i < BATCH_SIZE; i++) {
                for (int j = 0; j < h_numNodes[i]; j++) {
                    if (results[i * PAGE_SIZE + j]) {
                        count++;
                    }
                }
            }
            pageCount = 0;
        }

        currPage = currPage->next;
        pageVisted++;
    }

    if (pageCount != 0) {
        cudaMemcpy(d_pages, h_pages, pageCount * sizeof(Node*), cudaMemcpyHostToDevice);
        cudaMemcpy(d_numNodes, h_numNodes, pageCount * sizeof(int), cudaMemcpyHostToDevice);

        dim3 blockSize(PAGE_SIZE);
        dim3 gridSize(pageCount);
        filterNodes<<<gridSize, blockSize>>>(d_pages, d_numNodes, topLatitude, leftLongitude,
                                             bottomLatitude, rightLongitude, d_results);

        bool* results = new bool[pageCount * PAGE_SIZE];

        cudaMemcpy(results, d_results, pageCount * PAGE_SIZE * sizeof(bool),
                   cudaMemcpyDeviceToHost);

        for (int i = 0; i < pageCount; i++) {
            for (int j = 0; j < h_numNodes[i]; j++) {
                if (results[i * PAGE_SIZE + j]) {
                    count++;
                }
            }
        }
    }

    cudaFree(d_pages);
    cudaFree(d_numNodes);
    cudaFree(d_results);

    cout << "Pages visited: " << pageVisted << endl;
    return count;
}

vector<Node*> PsfcIndex::findNodesNamed_Host(tuple<double, double> topLeft,
                                             tuple<double, double> bottomRight, const char* name) {
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
