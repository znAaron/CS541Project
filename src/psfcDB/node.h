#ifndef NODE_H
#define NODE_H

#include <cstdint>
#include <cstring>
#include <limits>

#define MAX_NAME_LEN 32
#define MAX_LONG 180.0
#define MAX_LAT 90.0

struct Node {
    uint32_t id;
    uint32_t type;
    uint64_t zIndex;
    double longitude;
    double latitude;
    char name[MAX_NAME_LEN];

    Node(uint32_t nid, uint32_t ntype, double nlong, double nlat, char* nname) {
        // assign value
        id = nid;
        type = ntype;
        longitude = nlong;
        latitude = nlat;

        // copy name
        strncpy(name, nname, MAX_NAME_LEN);

        // Calculate the z index for z curve
        // Normalize and scale the longitude and latitude to the range [0, 1]
        double normalizedLongitude = (nlong + MAX_LONG) / (2.0 * MAX_LONG);
        double normalizedLatitude = (nlat + MAX_LAT) / (2.0 * MAX_LAT);

        // Convert the normalized values to uint64_t
        uint64_t x =
            static_cast<uint64_t>(normalizedLongitude * std::numeric_limits<uint64_t>::max());
        uint64_t y =
            static_cast<uint64_t>(normalizedLatitude * std::numeric_limits<uint64_t>::max());
        zIndex = 0;

        for (int i = 0; i < sizeof(uint64_t) * 8; i++) {
            // Extract the i-th bit of x and y
            uint64_t bitX = (x & (1ull << i)) >> i;
            uint64_t bitY = (y & (1ull << i)) >> i;

            // Interleave the bits of x and y to form the i-th bit of z
            zIndex |= (bitX << (2 * i));
            zIndex |= (bitY << ((2 * i) + 1));
        }
    }
};
#endif