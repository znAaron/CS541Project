#include <jsoncpp/json/json.h>
#include <jsoncpp/json/reader.h>
#include <jsoncpp/json/value.h>
#include <jsoncpp/json/writer.h>

#include <iostream>
#include <string>

#include "httplib.h"
#include "index.h"

using namespace std;
using namespace httplib;

class PsfcServer {
   public:
    PsfcServer() {
        // Initialize the PsfcIndex object
        psfcIndex = new PsfcIndex();
    }

    ~PsfcServer() { delete psfcIndex; }

    void start() {
        // Create an HTTP server and define the request handler
        Server server;
        server.Post("/", [&](const Request& req, Response& res) {
            string response = processRequest(req.body);
            res.set_content(response, "application/json");
        });

        // Start the server and listen on localhost:8080
        server.listen("localhost", 8080);
    }

    string processRequest(const string& request) {
        Json::Reader reader;
        Json::Value root;
        if (!reader.parse(request, root)) {
            return "Invalid JSON";
        }

        string command = root["command"].asString();
        Json::Value response;

        if (command == "addNode") {
            // Extract the node details from the request
            uint32_t id = root["id"].asUInt();
            uint32_t type = root["type"].asUInt();
            double latitude = root["latitude"].asDouble();
            double longitude = root["longitude"].asDouble();
            string name = root["name"].asString().substr(0, 31);  // Limit the name to 31 characters

            // Create a Node object and add it to the PsfcIndex
            Node* node = new Node(id, type, latitude, longitude, name.c_str());
            psfcIndex->addNode(node);

            response["status"] = "success";
        } else if (command == "flushAll") {
            // Flush all nodes from the PsfcIndex
            psfcIndex->flushAll();

            response["status"] = "success";
        } else if (command == "findNodes_device") {
            // Extract the top left and bottom right coordinates from the request
            double topLeftLatitude = root["topLeft"][0].asDouble();
            double topLeftLongitude = root["topLeft"][1].asDouble();
            double bottomRightLatitude = root["bottomRight"][0].asDouble();
            double bottomRightLongitude = root["bottomRight"][1].asDouble();

            // Call the findNodes_device function and store the result
            int result =
                psfcIndex->findNodes_Host(make_tuple(topLeftLatitude, topLeftLongitude),
                                          make_tuple(bottomRightLatitude, bottomRightLongitude));

            response["status"] = "success";
            response["result"] = result;
        } else if (command == "numPages") {
            // Get the number of pages from the PsfcIndex
            int num = psfcIndex->numPages();

            response["status"] = "success";
            response["result"] = num;
        } else {
            response["status"] = "error";
            response["message"] = "Invalid command";
        }

        Json::FastWriter writer;
        return writer.write(response);
    }

   private:
    PsfcIndex* psfcIndex;
};

int main() {
    PsfcServer server;
    server.start();

    return 0;
}
