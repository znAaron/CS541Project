#ifndef NODE_H
#define NODE_H

#include <cstdint>
#include <cstring>
#include <limits>
#include <tuple>

using namespace std;

#define MAX_NAME_LEN 32
#define MAX_LONG 180.0
#define MAX_LAT 90.0

struct Node {
    double latitude;
    double longitude;

    uint32_t id;
    uint32_t type;
    uint64_t zIndex;
    char name[MAX_NAME_LEN];

    Node(uint32_t nid, uint32_t ntype, double nlat, double nlong, const char* nname);

    // return true if the node is with in the rectangle defined by the coordinates of the topLeft
    // corner and the bottomRight corner
    bool inRegion(tuple<double, double> topLeft, tuple<double, double> bottomRight);

    bool inRegionFlat(double topLatitude, double leftLongitude, double bottomLatitude,
                      double rightLongitude);

    bool nameContains(const char* query);

    string to_string();
};

bool compareNodes(const Node& a, const Node& b);

uint64_t coordToZIndex(double latitude, double longitude);

Node* generateRandomNode();  // generate a random node for testing

Node* generateRandomNamedNode();  // generate a random node with a random name for testing

#endif