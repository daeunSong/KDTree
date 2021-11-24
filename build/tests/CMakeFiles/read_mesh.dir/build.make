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
include tests/CMakeFiles/read_mesh.dir/depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/read_mesh.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/read_mesh.dir/flags.make

tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o: tests/CMakeFiles/read_mesh.dir/flags.make
tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o: ../tests/read_mesh.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/daeun/devel/tspArt/KDTree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && /usr/bin/g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/read_mesh.dir/read_mesh.cpp.o -c /home/daeun/devel/tspArt/KDTree/tests/read_mesh.cpp

tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/read_mesh.dir/read_mesh.cpp.i"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/daeun/devel/tspArt/KDTree/tests/read_mesh.cpp > CMakeFiles/read_mesh.dir/read_mesh.cpp.i

tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/read_mesh.dir/read_mesh.cpp.s"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/daeun/devel/tspArt/KDTree/tests/read_mesh.cpp -o CMakeFiles/read_mesh.dir/read_mesh.cpp.s

tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.requires:

.PHONY : tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.requires

tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.provides: tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.requires
	$(MAKE) -f tests/CMakeFiles/read_mesh.dir/build.make tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.provides.build
.PHONY : tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.provides

tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.provides.build: tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o


# Object files for target read_mesh
read_mesh_OBJECTS = \
"CMakeFiles/read_mesh.dir/read_mesh.cpp.o"

# External object files for target read_mesh
read_mesh_EXTERNAL_OBJECTS =

bin/read_mesh: tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o
bin/read_mesh: tests/CMakeFiles/read_mesh.dir/build.make
bin/read_mesh: lib/libKDTree.so
bin/read_mesh: tests/CMakeFiles/read_mesh.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/daeun/devel/tspArt/KDTree/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../bin/read_mesh"
	cd /home/daeun/devel/tspArt/KDTree/build/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/read_mesh.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/read_mesh.dir/build: bin/read_mesh

.PHONY : tests/CMakeFiles/read_mesh.dir/build

tests/CMakeFiles/read_mesh.dir/requires: tests/CMakeFiles/read_mesh.dir/read_mesh.cpp.o.requires

.PHONY : tests/CMakeFiles/read_mesh.dir/requires

tests/CMakeFiles/read_mesh.dir/clean:
	cd /home/daeun/devel/tspArt/KDTree/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/read_mesh.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/read_mesh.dir/clean

tests/CMakeFiles/read_mesh.dir/depend:
	cd /home/daeun/devel/tspArt/KDTree/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/daeun/devel/tspArt/KDTree /home/daeun/devel/tspArt/KDTree/tests /home/daeun/devel/tspArt/KDTree/build /home/daeun/devel/tspArt/KDTree/build/tests /home/daeun/devel/tspArt/KDTree/build/tests/CMakeFiles/read_mesh.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/read_mesh.dir/depend
