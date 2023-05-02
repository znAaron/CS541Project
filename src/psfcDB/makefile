# Makefile

# Compiler and flags
CUDA := nvcc
CUDAFLAGS := -arch=sm_89 -std=c++11 -ljsoncpp
GXX := g++
GXXFLAGS := -std=c++11 -ljsoncpp

# Source files
CPP_SRCS := memPage.cpp memPageList.cpp node.cpp tester.cpp server.cpp
TEST_SRCS := memPage.cpp memPageList.cpp node.cpp tester.cpp
SERVER_SRCS := memPage.cpp memPageList.cpp node.cpp server.cpp
CU_SRCS := index.cu 

# Object files
OBJS := $(CPP_SRCS:.cpp=.o) $(CU_SRCS:.cu=.o)
TEST_OBJS := $(TEST_SRCS:.cpp=.o) $(CU_SRCS:.cu=.o)
SERVER_OBJS := $(SERVER_SRCS:.cpp=.o) $(CU_SRCS:.cu=.o)

# TESTutable name
TEST := tester
SERVER := psfcServer

.PHONY: all test clean

# Default target
all: $(TEST) $(SERVER)
server: $(SERVER)
test: $(TEST)

# Build the main TESTutable
$(TEST): $(TEST_OBJS)
	$(CUDA) $(CUDAFLAGS) $^ -o $@

# Build the main TESTutable
$(SERVER): $(SERVER_OBJS)
	$(CUDA) $(CUDAFLAGS) $^ -o $@

# Compile CUDA source files
%.o: %.cpp
	$(GXX) $(GXXFLAGS) -c $< -o $@

%.o: %.cu
	$(CUDA) $(CUDAFLAGS) -c $< -o $@

# Clean generated files
clean:
	rm -f $(OBJS) $(TEST)