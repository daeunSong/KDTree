# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/daeun/devel/tspArt/KDTree

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/daeun/devel/tspArt/KDTree/build

# Include any dependencies generated for this target.
include tests/CMakeFiles/construction_time.dir/depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/construction_time.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/construction_time.dir/flags.make

tests/CMakeFiles/construction_time.dir/construction_time.cpp.o: tests/CMakeFiles/construction_time.dir/flags.make
tests/CMakeFiles/construction_time.dir/construction_time.cpp.o: ../tests/construction_time.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/daeun/devel/tspArt/KDTree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object tests/CMakeFiles/construction_time.dir/construction_time.cpp.o"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && /usr/bin/g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/construction_time.dir/construction_time.cpp.o -c /home/daeun/devel/tspArt/KDTree/tests/construction_time.cpp

tests/CMakeFiles/construction_time.dir/construction_time.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/construction_time.dir/construction_time.cpp.i"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/daeun/devel/tspArt/KDTree/tests/construction_time.cpp > CMakeFiles/construction_time.dir/construction_time.cpp.i

tests/CMakeFiles/construction_time.dir/construction_time.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/construction_time.dir/construction_time.cpp.s"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/daeun/devel/tspArt/KDTree/tests/construction_time.cpp -o CMakeFiles/construction_time.dir/construction_time.cpp.s

tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.requires:

.PHONY : tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.requires

tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.provides: tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.requires
	$(MAKE) -f tests/CMakeFiles/construction_time.dir/build.make tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.provides.build
.PHONY : tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.provides

tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.provides.build: tests/CMakeFiles/construction_time.dir/construction_time.cpp.o


# Object files for target construction_time
construction_time_OBJECTS = \
"CMakeFiles/construction_time.dir/construction_time.cpp.o"

# External object files for target construction_time
construction_time_EXTERNAL_OBJECTS =

bin/construction_time: tests/CMakeFiles/construction_time.dir/construction_time.cpp.o
bin/construction_time: tests/CMakeFiles/construction_time.dir/build.make
bin/construction_time: lib/libKDTree.so
bin/construction_time: tests/CMakeFiles/construction_time.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/daeun/devel/tspArt/KDTree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../bin/construction_time"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/construction_time.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/construction_time.dir/build: bin/construction_time

.PHONY : tests/CMakeFiles/construction_time.dir/build

tests/CMakeFiles/construction_time.dir/requires: tests/CMakeFiles/construction_time.dir/construction_time.cpp.o.requires

.PHONY : tests/CMakeFiles/construction_time.dir/requires

tests/CMakeFiles/construction_time.dir/clean:
	cd /home/daeun/devel/tspArt/KDTree/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/construction_time.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/construction_time.dir/clean

tests/CMakeFiles/construction_time.dir/depend:
	cd /home/daeun/devel/tspArt/KDTree/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/daeun/devel/tspArt/KDTree /home/daeun/devel/tspArt/KDTree/tests /home/daeun/devel/tspArt/KDTree/build /home/daeun/devel/tspArt/KDTree/build/tests /home/daeun/devel/tspArt/KDTree/build/tests/CMakeFiles/construction_time.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/construction_time.dir/depend

