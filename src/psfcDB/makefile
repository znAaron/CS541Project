# Makefile

# Compiler and flags
CXX := nvcc
CXXFLAGS := -arch=sm_89

# Source files
SRCS := index.cpp memPage.cpp memPageList.cpp node.cpp tester.cpp

# Object files
OBJS := $(SRCS:.cpp=.o)

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

# Run the tester program
test: $(EXEC)
	./$(EXEC)

# Clean generated files
clean:
	rm -f $(OBJS) $(EXEC)