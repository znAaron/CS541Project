# Makefile

# Compiler and flags
CC = g++
CFLAGS = -Wall -Wextra -std=c++11

# Executable name
EXECUTABLE = tester

# Source files
SRCS = index.cpp tester.cpp

# Object files
OBJS = $(SRCS:.cpp=.o)

# Default rule
all: $(EXECUTABLE)

# Rule to compile object files
%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

# Rule to link the executable
$(EXECUTABLE): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

# Clean rule
clean:
	rm -f $(OBJS) $(EXECUTABLE)
