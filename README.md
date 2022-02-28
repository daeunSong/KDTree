# KDTree

Simple C++ static KD-Tree implementation with minimal functionality.

- points are given as STL vectors (and inserted in their own STL vector) so supports n-dimensional points for any n
- makes full trees, (i.e. does not cut-off the branching at some arbitrary level) giving the nearest neighbor query have (strong) logarithmic complexity.
- builds the tree in one go (does not support adding nodes, the tree is built from a list of points and cannot be altered afterwards)
- points are assumed to be STL vectors
- it provides the following queries:
	- nearest neighbor
	- neighbors within a given distance

## Build and compile

```shell
mkdir build && cd build
cmake ..
make -j4
```
This will generate the executable files in `build/bin` directory. 


- Following should be executed in `build` directory:
```shell
bin/./generate_input
```
Change ```WALL_OBJ```, ```DRAWING_TXT```, ```OUTPUT_TXT``` if you want to test out on different wall and drawing input.\
The drawing coordinates should be transformed on line 154 to fit the wall. (It will later be altered -- change wall coordinate to fit the drawing)\


- Following should be executed in `tests` directory:

```python plot.py```  plots wall and drawing 3d coordinates\
```python plot_input.py```  plots drawing 2d coordinates\
```python plot_output.py``` plots drawing 3d coordinates\
```python plot_wall.py``` plots wall\


## License and copyright

© J. Frederico Carvalho
Licensed under the [BSD3 License](LICENSE)
