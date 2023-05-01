# Makefile

# Compiler and flags
CXX := nvcc
CXXFLAGS := -arch=sm_89 -std=c++11 -lineinfo

# Source files
CPP_SRCS := memPage.cpp memPageList.cpp node.cpp tester.cpp
CU_SRCS := index.cu 

# Object files
OBJS := $(CPP_SRCS:.cpp=.o) $(CU_SRCS:.cu=.o)

# Executable name
EXEC := myprogram

.PHONY: all test clean

# Default target
all: $(EXEC)

# Build the main executable
$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile CUDA source files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

%.o: %.cu
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Run the tester program
test: $(EXEC)
	./$(EXEC)

# Clean generated files
clean:
	rm -f $(OBJS) $(EXEC)