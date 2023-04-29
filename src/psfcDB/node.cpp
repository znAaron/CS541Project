#include "node.h"

Node::Node(uint32_t nid, uint32_t ntype, double nlat, double nlong, const char* nname) {
    // assign value
    id = nid;
    type = ntype;
    latitude = nlat;
    longitude = nlong;

    // copy name
    strncpy(name, nname, MAX_NAME_LEN);

    // Calculate the z index for z curve
    zIndex = coordToZIndex(latitude, longitude);
}

bool Node::inRegion(tuple<double, double> topLeft, tuple<double, double> bottomRight) {
    double topLatitude = std::get<0>(topLeft);
    double leftLongitude = std::get<1>(topLeft);
    double bottomLatitude = std::get<0>(bottomRight);
    double rightLongitude = std::get<1>(bottomRight);

    // Check if the node is within the latitude and longitude range of the rectangle
    if (latitude >= bottomLatitude && latitude <= topLatitude && longitude >= leftLongitude &&
        longitude <= rightLongitude) {
        return true;
    }
    return false;
}

bool Node::nameContains(const char* query) {
    if (strstr(name, query) != nullptr) {
        return true;
    }
    return false;
}

bool compareNodes(const Node& a, const Node& b) { return a.zIndex < b.zIndex; }

uint64_t coordToZIndex(double latitude, double longitude) {
    // Normalize and scale the longitude and latitude to the range [0, 1]
    double normalizedLongitude = (longitude + MAX_LONG) / (2.0 * MAX_LONG);
    double normalizedLatitude = (latitude + MAX_LAT) / (2.0 * MAX_LAT);

    // Convert the normalized values to uint64_t
    uint64_t x = static_cast<uint64_t>(normalizedLongitude * std::numeric_limits<uint64_t>::max());
    uint64_t y = static_cast<uint64_t>(normalizedLatitude * std::numeric_limits<uint64_t>::max());
    uint64_t zIndex = 0;

    for (int i = 0; i < 64; i++) {
        // Extract the i-th bit of x and y
        uint64_t bitX = (x & (1ull << i)) >> i;
        uint64_t bitY = (y & (1ull << i)) >> i;

        // Interleave the bits of x and y to form the i-th bit of z
        zIndex |= (bitX << (2 * i));
        zIndex |= (bitY << ((2 * i) + 1));
    }

    return zIndex;
}

Node* generateRandomNode() {
    // Generate random node
    uint32_t id = rand();
    uint32_t type = rand();
    double latitude = (double)rand() / RAND_MAX * 180.0 - 90.0;
    double longitude = (double)rand() / RAND_MAX * 360.0 - 180.0;
    char name[MAX_NAME_LEN];
    for (int i = 0; i < MAX_NAME_LEN - 1; i++) {
        name[i] = rand() % 26 + 'a';
    }
    name[MAX_NAME_LEN] = '\0';
    return new Node(id, type, latitude, longitude, name);
};

Node* generateRandomNamedNode() {
    // Generate random node
    uint32_t id = rand();
    uint32_t type = rand();
    double latitude = (double)rand() / RAND_MAX * 180.0 - 90.0;
    double longitude = (double)rand() / RAND_MAX * 360.0 - 180.0;
    return new Node(id, type, latitude, longitude,
                    "This is the Bob's Fancy Coffee Shop in the middle of nowhere");
};